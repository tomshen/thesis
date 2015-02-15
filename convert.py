#!/usr/bin/env python
import os.path as path
import sys


def ground_graph(graph_edges, seeds, labels):
    edges = []
    nodes = {}
    node_label = 1
    features = [
        'id(trueLoop)',
        'id(trueLoopRestart)',
        'fixedWeight',
        'id(restart)',
        'id(alphaBooster)'
    ]

    for node1, node2, weight in graph_edges:
        if node1 not in nodes:
            nodes[node1] = node_label
            node_label += 1
        if node2 not in nodes:
            nodes[node2] = node_label
            node_label += 1
        n1 = nodes[node1]
        n2 = nodes[node2]
        edges.append((n1, n2, [len(features)]))
        edges.append((n2, n1, [len(features)]))
        features.append('w({0},{1})'.format(node1, node2))

    return [{
        'query_vec_keys': [1],
        'pos_nodes': [nodes[n] for n,l in seeds.items() if l == label],
        'neg_nodes': [nodes[n] for n,l in seeds.items() if l != label],
        'node_count': len(nodes),
        'edges': edges,
        'features': features
    } for label in labels]


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


def parse_junto(config_file):
    config = parse_junto_config(config_file)
    edges = parse_junto_graph(config['graph_file'])
    seeds = dict((node, label) for node, label, weight in
        parse_junto_graph(config['seed_file']))
    return edges, seeds


def convert_junto_to_proppr(junto_config_file, program_dir):
    name = path.basename(junto_config_file).split('.')[0]
    junto_edges, seeds = parse_junto(junto_config_file)
    labels = set(seeds.itervalues())

    with open(path.join(program_dir, name + '.cfacts'), 'w') as facts_fp:
        for label in labels:
            facts_fp.write('isLabel\t{0}\n'.format(label))

    with open(path.join(program_dir, name + '.graph'), 'w') as graph_fp:
        for node1, node2, weight in junto_edges:
            graph_fp.write('\t'.join(['edge', node1, node2]) + '\n')
        for node, label in seeds.items():
            graph_fp.write('\t'.join(['seed', node, label]) + '\n')

    grounded_graph = ground_graph(junto_edges, seeds, labels)

    # TODO: Fix
    grounded_strings = ('\t'.join([
        name, # query
        ','.join(str(i) for i in proppr_query['query_vec_keys']),
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
    convert_junto_to_proppr(sys.argv[1], sys.argv[2])
