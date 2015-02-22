#!/usr/bin/env python
import itertools
import os.path as path
import random
import sys


def fresh_gen():
    label = [0]
    def fresh():
        label[0] += 1
        return label[0]
    return fresh


def ground_graph(graph_edges, seeds, labels):
    graphs = []
    for label in labels:
        print 'Grounding label {0}'.format(label),
        edges = []
        nodes = {}
        fresh = fresh_gen()

        features = [
            'seed',
            'id(trueLoop)',
            'id(trueLoopRestart)',
            'fixedWeight',
            'id(restart)',
            'id(alphaBooster)'
        ] # 1-indexed

        for node1, node2, weight in graph_edges:
            if node1 not in nodes:
                nodes[node1] = fresh()
            if node2 not in nodes:
                nodes[node2] = fresh()
            n1 = nodes[node1]
            n2 = nodes[node2]
            # features.append('edge({0},{1})'.format(node1, node2))
            edges.append((n1, n2, [4]))
            edges.append((n2, n1, [4]))

        start_node = fresh()

        for node in nodes:
            if node in seeds and seeds[node] == label:
                edges.append((start_node, nodes[node], [1]))

        graphs.append({
            'query': 'assoc({0},X-1)  #v:[?].'.format(label),
            'pos_nodes': [start_node],
            'neg_nodes': [],
            'node_count': len(nodes),
            'edges': edges,
            'features': features
        })
        print 'done'

    return graphs


def parse_junto_config(config_file):
    config = dict()
    with open(config_file) as config_fp:
        for line in config_fp:
            try:
                key, value = line.strip().split(' = ')
                config[key] = value
            except:
                continue
    return config


def parse_junto_graph(graph_file):
    edges = []
    with open(graph_file) as graph_fp:
        for line in graph_fp:
            node1, node2, weight = line.split()
            edges.append((node1, node2, weight))
    return edges


def parse_junto(config_file, prop=None):
    config = parse_junto_config(config_file)
    edges = parse_junto_graph(config['graph_file'])
    if prop:
        edges = random.sample(edges, int(len(edges) * prop))
    seeds = dict((node, label) for node, label, weight in
        parse_junto_graph(config['seed_file']))
    return edges, seeds


def convert_junto_to_proppr(junto_config_file, program_dir, prop):
    name = path.basename(junto_config_file).split('.')[0]
    junto_edges, seeds = parse_junto(junto_config_file, prop)
    labels = set(seeds.itervalues())

    grounded_graph = ground_graph(junto_edges, seeds, labels)

    grounded_strings = ('\t'.join([
        proppr_query['query'],
        ','.join(['1']), # query_vec
        ','.join(str(i) for i in proppr_query['pos_nodes']),
        ','.join(str(i) for i in proppr_query['neg_nodes']),
        str(proppr_query['node_count']),
        str(len(proppr_query['edges'])),
        ':'.join(proppr_query['features']),
        '\t'.join('{0}->{1}:{2}'.format(n1, n2, ','.join(str(i) for i in f))
            for n1, n2, f in proppr_query['edges'])
    ]) + '\n' for proppr_query in grounded_graph)
    with open(path.join(program_dir, name + '.grounded'), 'w') as grounded_fp:
        for s in grounded_strings:
            grounded_fp.write(s)


if __name__ == '__main__':
    convert_junto_to_proppr(sys.argv[1], sys.argv[2],
        float(sys.argv[3]) if len(sys.argv) >= 4 else None)
