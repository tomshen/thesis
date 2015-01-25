#!/usr/bin/env python
from collections import defaultdict
import random


def make_seed_cfacts(perc=10):
    with open('20NG_seed_{0}perc.cfacts'.format(perc), 'w') as outfile:
        with open('data/20NG.gold') as infile:
            for line in infile:
                if random.random() < perc/100.0:
                    d, l, _ = line.split()
                    label = 'l' + l
                    doc = 'd' + d
                    outfile.write('seed\t{0}\t{1}\n'.format(label, doc))


def make_queries():
    labels = defaultdict(list)
    with open('data/20NG.gold') as infile:
        for line in infile:
            d, l, _ = line.split()
            label = 'l' + l
            doc = 'd' + d
            labels[label].append(doc)
    with open('20NG_test.data', 'w') as outfile:
        for label, docs in labels.items():
            outfile.write('assoc({0},X)\t'.format(label)
                + '\t'.join('+assoc({0},{1})'.format(label, doc) for doc in docs)
                + '\n')

if __name__ == '__main__':
    make_seed_cfacts()
    make_queries()
