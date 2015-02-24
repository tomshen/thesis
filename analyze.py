#!/usr/bin/env python
from collections import defaultdict
import json
import re
import sys

import convert

def load_results(results_file):
    results = defaultdict(set)
    with open(results_file) as results_fp:
        for line in results_fp:
            try:
                node, query = line.strip().split('\t')
                results[query].add(node)
            except:
                pass
    return results


def load_map(map_file):
    node_map = {}
    with open(map_file) as map_fp:
        while True:
            try:
                query = map_fp.readline().strip()
                nodes = json.loads(map_fp.readline())
                node_map[query] = nodes
            except:
                break
    return node_map


def convert_results(raw_results, node_map):
    results = {}
    for query, nodes in raw_results.items():
        try:
            label = re.match(r'assoc\((.*),X-1\)', query).group(1)
        except AttributeError:
            continue
        label_node_map = node_map[query]
        results[label] = set((label_node_map[unicode(node)]
                for node in nodes))
    return results


def analyze_results(results, doc_labels):
    for label, nodes in results.items():
        num_correct = 0
        num_docs = 0
        for node in nodes:
            if node[0] == 'd':
                num_docs += 1
                if doc_labels[node] == label:
                    num_correct += 1
        print '%s: %.2f%% correct' % (label, float(100 * num_correct) / num_docs)



if __name__ == '__main__':
    raw_results = load_results(sys.argv[1])
    node_map = load_map(sys.argv[2])
    results = convert_results(raw_results, node_map)
    doc_labels = dict((d, l) for d, l, _ in
            convert.parse_junto_graph('data/20NG.gold'))
    analyze_results(results, doc_labels)

