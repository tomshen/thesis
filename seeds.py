#!/usr/bin/env python
import argparse
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Make seeds from a Junto test file')
    parser.add_argument('test_file', type=file, help='Junto test file')
    parser.add_argument('-p', dest='percent', type=float, help='Percent seeds',
            required=True)
    parser.add_argument('-o', dest='output_file',
            type=argparse.FileType('w'), required=True)

    args = parser.parse_args()

    if args.percent.is_integer():
        proportion = args.percent / 100
    else:
        proportion = args.percent
    for line in args.test_file:
        if random.random() < proportion:
            args.output_file.write(line)

    args.test_file.close()
    args.output_file.close()
