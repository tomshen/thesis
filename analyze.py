#!/usr/bin/env python
import argparse
import itertools

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


def calculate_mrr(results, node_labels):
    """ calculates MRR for each label """
    Q = len(node_labels)
    inverse_rank_sum = 0.0
    for node, labels in results.items():
        if node in node_labels:
            true_label = node_labels[node]
            if true_label in labels:
                if  '__DUMMY__' in labels and labels.index('__DUMMY__') < labels.index(true_label):
                    inverse_rank_sum += 1.0 / (labels.index(true_label))
                else:
                    inverse_rank_sum += 1.0 / (labels.index(true_label) + 1)
    mrr = inverse_rank_sum / Q
    return mrr


def calculate_precision(results, node_labels, all_labels):
    total_predicted = {l: 0 for l in all_labels}
    correct_predicted = {l: 0 for l in all_labels}
    for node, labels in results.items():
        if node in node_labels:
            true_label = node_labels[node]
            total_predicted[true_label] += 1
            if true_label in labels and true_label == labels[0] or (len(labels) > 1 and '__DUMMY__' == labels[0] and true_label == labels[1]):
                correct_predicted[true_label] += 1
    total_precision = 0.0
    for l in all_labels:
        total_precision += float(correct_predicted[l]) / total_predicted[l]
    return total_precision / len(labels)


def calculate_recall(results, node_labels, all_labels):
    total_true = {l: 0 for l in all_labels}
    correct_predicted = {l: 0 for l in all_labels}
    for node, true_label in node_labels.items():
        total_true[true_label] += 1
        if node in results and true_label in results[node] and (
                true_label == results[node][0] or (len(results[node]) > 1 and '__DUMMY__' == results[node][0] and true_label == results[node][1])):
            correct_predicted[true_label] += 1
    total_recall = 0.0
    for l in all_labels:
        total_recall += float(correct_predicted[l]) / total_true[l]
    return total_recall / len(labels)


def parse_results_file(results_file, test_file):
    results = parse_results(results_file)
    doc_labels = parse_test_file(test_file)
    labels = set(doc_labels.itervalues())
    return results, doc_labels, labels


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

    results, node_labels, labels = parse_results_file(args.results_file, test_file)
    print calculate_mrr(results, node_labels),
    print '\t',
    print calculate_precision(results, node_labels, labels),
    print '\t',
    print calculate_recall(results, node_labels, labels)
    args.results_file.close()
    test_file.close()
