#!/usr/bin/env python
import argparse

import convert


def parse_results(results_file):
    results = {}
    for line in results_file:
        toks = line.strip().split('\t')
        node = toks[0]
        labels = toks[1:]
        results[node] = labels
    return results


def parse_test_file(test_file):
    return dict((d, l) for d,l,_ in convert.parse_junto_graph(test_file))


def analyze_results(results, node_labels):
    """ calculates MRR for each label """
    Q = len(node_labels)
    inverse_rank_sum = 0.0
    for node, labels in results.items():
        if node in node_labels:
            true_label = node_labels[node]
            if true_label in labels:
                inverse_rank_sum += 1.0 / (labels.index(true_label) + 1)
    mrr = inverse_rank_sum / Q
    print 'MRR', mrr
    return mrr


def analyze_results_file(results_file, test_file):
    results = parse_results(results_file)
    doc_labels = parse_test_file(test_file)
    analyze_results(results, doc_labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyze a results file from Junto or ProPPR SRW.')
    parser.add_argument('results_file', type=file, help='Results file')
    parser.add_argument('--config', dest='junto_config', type=file,
        nargs='?', help='Junto config file')
    parser.add_argument('--test', dest='junto_test_file', type=file,
        nargs='?', help='Junto test_file')
    args = parser.parse_args()

    if args.junto_config:
        test_file = open(convert.parse_junto_config(args.junto_config)['test_file'])
    elif args.junto_test_file:
        test_file = args.junto_test_file
    else:
        raise parser.error(
            'Must specify either a Junto config file or a Junto test file')

    analyze_results_file(args.results_file, test_file)
    args.results_file.close()
    test_file.close()
