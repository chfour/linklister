#!/usr/bin/env python3
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("start_url", type=str,
                    help="URL to start from")
parser.add_argument("-o", "--output", type=str, default="-",
                    help="output file to write to, - for stdout, default -")
args = parser.parse_args()

if args.output == "-":
    output = sys.stdout
else:
    output = open(args.output, "a")

with output:
    output.write(args.start_url + "\n")
