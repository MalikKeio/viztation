#!/usr/bin/env python3

import argparse
import logging

parser = argparse.ArgumentParser(description="Put your TeX and Bib files here to visualize the relationship tying them")
parser.add_argument('-t', '--tex', nargs='*', default=[], type=str, help="TeX files to load and link")
parser.add_argument('-b', '--bib', nargs='*', default=[], type=str, help="BiB files to load and link")
parser.add_argument('-v', '--verbose', action="store_true", help="Set output to verbose (debug)")
parser.add_argument('-s', '--scan', nargs='*', default=[], type=str, help="Scan a folder or more for TeX and BiB files (found files are added to possible --tex and --bib arguments)")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(filename="out.log", level=logging.DEBUG)

for directory in args.scan:
    import os
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".tex"):
                args.tex.append(os.path.join(root, f));
            if f.endswith(".bib"):
                args.bib.append(os.path.join(root, f));

if __name__ == "__main__":

    from latexparser import LaTexFiles
    from bibtexparser import BibTexFiles

    latexfiles = LaTexFiles(args.tex)
    bibtexfiles = BibTexFiles(args.bib)

    references = bibtexfiles.get_references(dictionary=True)


    import networkx as nx
    import matplotlib.pyplot as plt
    import interaction

    G = nx.Graph()
    elists = {}
    latexfile_node_list = []
    ref_node_list = []

    for latexfile in latexfiles.files:
        latexfile_node_list.append(latexfile)
        ref_id_count = {}
        for ref_id in latexfile.cites:
            # Should set and show weight
            if ref_id not in ref_id_count:
                ref_id_count[ref_id] = 1
            else:
                ref_id_count[ref_id] += 1
        for ref_id, count in ref_id_count.items():
            ref_node_list.append(ref_id)
            if count in elists:
                elists[count].append((latexfile, ref_id, count))
            else:
                elists[count] = [(latexfile, ref_id, count)]

    G.add_nodes_from(latexfile_node_list)
    G.add_nodes_from(ref_node_list)
    for weight, elist in elists.items():
        G.add_weighted_edges_from(elist)
    pos = nx.nx_agraph.graphviz_layout(G, prog='twopi', args='')
    interaction.InteractiveNodes(pos)
    interaction.InteractiveNode.set_reference_dict(references)

    nx.draw_networkx_nodes(G, pos, nodelist=latexfile_node_list, node_color='r')
    nx.draw_networkx_nodes(G, pos, nodelist=ref_node_list, node_color='b')
    edge_labels = {}
    for weight, elist in elists.items():
        nx.draw_networkx_edges(G, pos, edgelist=elist, width=weight)
        for edge in elist:
            edge_labels[(edge[0], edge[1])] = "%d" % weight
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.tick_params(which='both',bottom='off',top='off',labelbottom='off',left='off',right='off',labelleft='off')
    plt.show()
