#!/usr/bin/env python

label_map = {
    'l1': set(['l1']), # alt.*
    'l2': set(['l2', 'l3', 'l4', 'l5', 'l6']), # comp.*
    'l3': set(['l7']), # misc.*,
    'l4': set(['l8', 'l9', 'l10', 'l11']), # rec.*
    'l5': set(['l12', 'l13', 'l14', 'l15']), # sci.*
    'l6': set(['l16']), # soc.*
    'l7': set(['l17', 'l18', 'l19', 'l20']) # talk.*
}

with open('data/20NG.gold') as f:
    for line in f:
        toks = line.strip().split('\t')
        for new_label, old_labels in label_map.items():
            if toks[1] in old_labels:
                print '{0}\t{1}\t{2}'.format(toks[0], new_label, toks[2])
                break
