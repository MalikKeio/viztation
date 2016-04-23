#!/usr/bin/env python3

import argparse
import logging

parser = argparse.ArgumentParser(description="Put your TeX and Bib files here to visualize the relationship tying them")
parser.add_argument('-t', '--tex', nargs='*', default=[], type=str, help="TeX files to load and link")
parser.add_argument('-b', '--bib', nargs='*', default=[], type=str, help="BiB files to load and link")
parser.add_argument('-v', '--verbose', action="store_true", help="Set output to verbose (debug)")

args = parser.parse_args()

if(args.verbose):
    logging.basicConfig(filename="out.log", level=logging.DEBUG)

from latexparser import LaTexFiles
from bibtexparser import BibTexFiles

latexfiles = LaTexFiles(args.tex)
bibtexfiles = BibTexFiles(args.bib)

references = bibtexfiles.get_references()

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

for latexfile in latexfiles.files:
    G.add_node(latexfile)
    for ref_id in latexfile.cites:
        G.add_node(ref_id)
        G.add_edge(latexfile, ref_id)

nx.draw(G)
plt.show()
