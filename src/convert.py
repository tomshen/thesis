#!/usr/bin/env python
import os.path as path
import sys


def create_proppr_graph(graph_edges, seeds):
    edges = []
    nodes = {}
    node_label = 1
    features = []

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

    return {
        'pos_nodes': [],
        'neg_nodes': [],
        'node_count': len(nodes),
        'edges': edges,
        'features': features
    }


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

    proppr_graph = create_proppr_graph(junto_edges, seeds)

    # TODO: Fix
    grounded_string = '\t'.join([
        name, # query
        '', # query_vec_keys
        ','.join(proppr_graph['pos_nodes']),
        ','.join(proppr_graph['neg_nodes']),
        str(proppr_graph['node_count']),
        str(len(proppr_graph['edges'])),
        ':'.join(proppr_graph['features']),
        '\t'.join('{0}->{1}:{2}'.format(n1, n2, ','.join(str(i) for i in f))
            for n1, n2, f in proppr_graph['edges'])
    ])
    with open(path.join(program_dir, name + '.grounded'), 'w') as grounded_fp:
        grounded_fp.write(grounded_string)


if __name__ == '__main__':
    convert_junto_to_proppr(sys.argv[1], sys.argv[2])
