#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Put your TeX and Bib files here to visualize the relationship tying them")
parser.add_argument('-t', '--tex', nargs='*', default=[], type=str, help="TeX files to load and link")
parser.add_argument('-b', '--bib', nargs='*', default=[], type=str, help="BiB files to load and link")

args = parser.parse_args()
