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
elist = []
latexfile_node_list = []
ref_node_list = []

for latexfile in latexfiles.files:
    latexfile_node_list.append(latexfile)
    for ref_id in latexfile.cites:
        ref_node_list.append(ref_id)
        # Should set and show weight
        elist.append((latexfile, ref_id, 1))

G.add_nodes_from(latexfile_node_list)
G.add_nodes_from(ref_node_list)
G.add_weighted_edges_from(elist)
pos = nx.graphviz_layout(G, prog='twopi', args='')

nx.draw_networkx_nodes(G, pos, nodelist=latexfile_node_list, node_color='r')
nx.draw_networkx_nodes(G, pos, nodelist=ref_node_list, node_color='b')
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos)

plt.axis('off')
plt.show()
