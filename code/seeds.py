#!/usr/bin/env python
import argparse
from collections import Counter
import math
import random

def make_random_seeds(test_file, proportion, output_file):
    for line in test_file:
        if random.random() < proportion:
            output_file.write(line)

def node_degrees(graph_file):
    degrees = Counter()
    for line in graph_file:
        toks = line.strip().split('\t')
        degrees[toks[0]] += 1
        degrees[toks[1]] += 1
    return degrees


def make_top_seeds(node_degrees, test_file, proportion, output_file):
    nodes = {}
    for line in test_file:
        toks = line.strip().split('\t')
        nodes[toks[0]] = (toks[1], toks[2])
    num_top_nodes = int(math.floor(len(nodes) * proportion))
    for node in list(reversed(sorted(nodes, key=node_degrees.get)))[:num_top_nodes]:
        output_file.write('{0}\t{1}\t{2}\n'.format(node, nodes[node][0], nodes[node][1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Make seeds from a Junto test file')
    parser.add_argument('test_file', type=file, help='Junto test file')
    parser.add_argument('-p', dest='percent', type=float, help='Percent seeds',
            required=True)
    parser.add_argument('--graph', dest='graph_file', type=file, help='Junto graph file')
    parser.add_argument('-o', dest='output_file',
            type=argparse.FileType('w'), required=True)

    args = parser.parse_args()

    if args.percent.is_integer():
        proportion = args.percent / 100
    else:
        proportion = args.percent
    if args.graph_file:
        degrees = node_degrees(args.graph_file)
        make_top_seeds(degrees, args.test_file, proportion, args.output_file)
        args.graph_file.close()
    else:
        make_random_seeds(args.test_file, proportion, args.output_file)

    args.test_file.close()
    args.output_file.close()
