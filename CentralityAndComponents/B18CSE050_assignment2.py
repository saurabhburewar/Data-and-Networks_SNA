"""
Social Network Analysis: Programming Assignment 2
Author: Saurabh Burewar (B18CSE050)

References: Networkx documentation https://networkx.org/documentation/stable/reference/index.html
            Stack overflow (for some unexpected errors)
"""

import networkx as nx
import csv
import gzip
import os
import requests
from tqdm import tqdm
import matplotlib.pyplot as plt


def close_cen(G):
    """
    """
    given = ['1', '7188', '430', '3026', '3134',
             '3010', '804', '160', '95', '377', '888']

    raw_close = {}
    nor_close = {}
    for n in given:
        sum_dist = 0
        for node in G.nodes:
            if n != node:
                try:
                    sum_dist += nx.shortest_path_length(G,
                                                        source=n, target=node)
                except nx.NetworkXNoPath:
                    continue

        raw_close[n] = 1 / sum_dist
        nor_close[n] = (nx.number_of_nodes(G) - 1) / sum_dist

    print()
    print("-------------- Closeness Centrality ------------------")
    print("Raw closeness Centrality - Node : closeness centrality")
    for key in raw_close:
        print("\t\t\t  ", key, " : ", raw_close[key])
    print()
    print("Normalized closeness centrality - Node : closeness centrality ")
    for key in raw_close:
        print("\t\t\t\t ", key, " : ", nor_close[key])


def betw_cen(G):
    """
    """
    given = ['1', '7188', '430', '3026', '3134',
             '3010', '804', '160', '95', '377', '888']

    betw = {}
    for n in tqdm(given):
        score = 0
        for node1 in tqdm(G.nodes):
            for node2 in G.nodes:
                if node1 != node2:
                    try:
                        path = nx.shortest_path(G, source=node1, target=node2)
                        if n in path:
                            score += 1
                    except nx.NetworkXNoPath:
                        continue

        betw[n] = score

    print()
    print("-------------- Betweeness Centrality -----------------")
    print("Betweeness centrality: ", betw)


def check_k_cores(G1, k):
    while(1):
        for node in list(G1.nodes):
            if G1.degree(node) < k:
                G1.remove_node(node)

        deglist = [x[1] for x in list(G1.degree())]
        if all(i >= k for i in deglist):
            return G1


def k_cores(G):
    """
    """
    print()
    print("--------------------- K-cores ------------------------")
    k = int(input("Enter 'k' from 0-20: "))
    G1 = G.copy()
    G1 = check_k_cores(G1, k)

    print("Drawing k-cores....")
    pos = nx.spring_layout(G1)
    nx.draw_networkx(G1, node_size=10, with_labels=False)
    plt.show()
    print("....K-cores displayed")


def lar_and_small_cliq(G):
    """
    """
    cliq_len = []
    max_count = 0
    min_count = 0
    for cliq in list(nx.find_cliques(G)):
        cliq_len.append(len(cliq))

    for i in cliq_len:
        if i == max(cliq_len):
            max_count += 1
        elif i == min(cliq_len):
            min_count += 1

    print()
    print("--------------------- Cliques ------------------------")
    print("Largest clique - Size: ", max(cliq_len), ", Number: ", max_count)
    print("Smallest clique - Size: ", min(cliq_len), ", Number: ", min_count)


def main():
    """
    The file for the data set is downlaoded from the snap url using
    "requests".

    The data is extracted from GZ format and csv is read row-wise. 
    Each row gives the source and destination of an edge with the 
    weights, the corresponding nodes and edges with weights are 
    created.

    Once the graph is created, all the functions are called.
    """

    # Downloading data set file
    Filename = "soc-sign-bitcoinalpha.csv.gz"
    url = "https://snap.stanford.edu/data/" + Filename
    print("Downloading data set file.....")
    with open(Filename, "wb") as file:
        r = requests.get(url)
        file.write(r.content)

    print()
    print("======================================================")
    print("         Bitcoin Alpha web of trust network")
    print("------------------------------------------------------")
    G = nx.DiGraph()

    # Creating graph
    with gzip.open('soc-sign-bitcoinalpha.csv.gz', 'rt') as file1:
        reader = csv.reader(file1)
        for row in reader:
            if row[0] not in G.nodes:
                G.add_node(row[0])
            if row[1] not in G.nodes:
                G.add_node(row[1])

            if (row[0], row[1]) not in G.edges:
                G.add_edge(row[0], row[1], weight=int(row[2]))

    # Calling network measures functions
    close_cen(G)
    lar_and_small_cliq(G.to_undirected())
    k_cores(G)
    betw_cen(G)

    # Remove downloaded file
    os.remove(Filename)

    print("======================================================")
    print()


if __name__ == "__main__":
    main()
