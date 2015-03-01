#!/usr/bin/env python
import argparse

import convert


def parse_results(results_file):
    return dict(line.split() for line in results_file)


def parse_test_file(test_file):
    return dict((d, l) for d,l,_ in convert.parse_junto_graph(test_file))


def analyze_results(results, doc_labels):
    for label, nodes in results.items():
        num_correct = 0
        num_docs = 0
        for node in nodes:
            if node[0] == 'd':
                num_docs += 1
                if doc_labels[node] == label:
                    num_correct += 1
        print '%s: %.2f%% correct' % (label, float(100 * num_correct)/num_docs)


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
        test_file = open(convert.parse_junto_config(junto_config)['test_file'])
    elif args.junto_test_file:
        test_file = args.junto_test_file
    else:
        raise parser.error(
            'Must specify either a Junto config file or a Junto test file')

    analyze_results_file(results_file, test_file)
    results_file.close()
    test_file.close()
