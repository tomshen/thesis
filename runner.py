#!/usr/bin/env python
import argparse
from collections import defaultdict
import json
import logging
import operator
import os
import os.path as path
import re
import subprocess

import convert


JUNTO_DIR = './lib/Junto'

PROPPR_DIR = './lib/ProPPR'
PROPPR_CP = '{0}/conf:{0}/bin:{0}/lib/*'.format(PROPPR_DIR)
DEFAULT_THREADS = 8

DEFAULT_MEM_SIZE = '32g'
DEFAULT_GRAPH_DIR = convert.DEFAULT_GRAPH_DIR

logger = logging.getLogger('runner')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def run_junto(config_filename, mem_size=DEFAULT_MEM_SIZE):
    junto_env = os.environ.copy()
    junto_env['JUNTO_DIR'] = path.join(os.getcwd(), 'lib/junto')
    junto_env['PATH'] = junto_env['JUNTO_DIR'] + ':' + junto_env['PATH']
    junto_env['JAVA_MEM_FLAG'] = '-Xmx{0}'.format(mem_size)
    logger.info('Running Junto on %s', config_filename)
    subprocess.call(['{0}/bin/junto'.format(JUNTO_DIR), 'config',
        config_filename], env=junto_env)
    with open(config_filename) as config_file:
        return convert_junto_results(
            convert.parse_junto_config(config_file)['output_file'])


def argmax(d):
    return max(d.iteritems(), key=operator.itemgetter(1))[0]


def convert_junto_results(output_filename):
    logger.info('Converting Junto results')
    def parse_label_scores(s):
        scores = s.split()
        return {scores[i]: float(scores[i+1]) for i in xrange(0, len(scores), 2)}

    with open_output_file(output_file) as f:
        data = csv.reader(f, delimiter='\t')
        nodes = {}
        for row in data:
            name = row[0]
            label_scores = parse_label_scores(row[3])
            nodes[name] = argmax(label_scores)
        return nodes


def run_srw_config(config_filename, mem_size=DEFAULT_MEM_SIZE,
    threads=DEFAULT_THREADS):
    logger.info('Converting %s to SRW graph', config_filename)
    with open(config_filename) as config_file:
        convert.convert_junto_to_proppr(config_file, DEFAULT_GRAPH_DIR)
    return run_srw(path.basename(config_filename).split('.')[0], mem_size)


def run_srw(data_name, mem_size=DEFAULT_MEM_SIZE, threads=DEFAULT_THREADS):
    srw_graph = path.join(DEFAULT_GRAPH_DIR, data_name + '.grounded')
    srw_output = path.join(DEFAULT_GRAPH_DIR, data_name + '.out.srw')
    node_mapping = path.join(DEFAULT_GRAPH_DIR, data_name + '.map')
    logger.info('Running SRW on %s', srw_graph)
    command = ['java', '-Xmx{0}'.format(mem_size), '-cp', PROPPR_CP,
        'edu.cmu.ml.proppr.Propagator', srw_graph, srw_output, str(threads)]
    logger.info('Calling: %s', ' '.join(command))
    subprocess.call(command)
    return convert_srw_results(srw_output, node_mapping)


def convert_srw_results(results_filename, node_map_filename):
    logger.info('Converting SRW results')
    def load_results(results_file):
        results = defaultdict(set)
        with open(results_file) as results_fp:
            for line in results_fp:
                try:
                    node, query = line.strip().split('\t', 1)
                    results[query].add(node)
                except:
                    pass
        return results


    def load_map(map_file):
        with open(map_file) as map_fp:
            return json.load(map_fp)


    raw_results = load_results(results_filename)
    node_map = load_map(node_map_filename)
    results = {}
    for query, nodes in raw_results.items():
        try:
            label = re.match(r'assoc\((.*),X-1\)', query).group(1)
        except AttributeError:
            continue
        if query in node_map:
            label_node_map = node_map[query]
            results[label] = set(label_node_map[unicode(node)]
                    for node in nodes)
        else:
            logger.error('Query not in node mapping: %s', query)
    return results


def write_results(results, output_file):
    for label, nodes in results.items():
        for node in nodes:
            output_file.write(node + '\t' + label + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Runs Junto or SRW')
    parser.add_argument('algorithm', choices=['junto', 'srw'])
    parser.add_argument('junto_config', type=str, help='Junto config file')
    parser.add_argument('--data', dest='data_name',
        help='Name of data set (looks for graph in {0})'.format(
            DEFAULT_GRAPH_DIR))
    parser.add_argument('--mem', dest='mem_size', default=DEFAULT_MEM_SIZE,
        help='Java memory size')
    parser.add_argument('-o', dest='output_file', type=argparse.FileType('w'),
        required=True)
    parser.add_argument('--threads', dest='threads', default=DEFAULT_THREADS,
        help='Number of threads for SRW')
    args = parser.parse_args()

    if not path.exists(DEFAULT_GRAPH_DIR):
        os.makedirs(DEFAULT_GRAPH_DIR)

    if args.algorithm == 'junto':
        results = run_junto(args.junto_config, args.mem_size)
    elif args.algorithm == 'srw':
        results = run_srw_config(args.junto_config, args.mem_size, args.threads)

    if args.output_file:
        write_results(results, args.output_file)
    args.output_file.close()
