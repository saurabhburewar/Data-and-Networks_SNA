"""
Social Network Analysis: Programming Assignment 3
Author: Saurabh Burewar (B18CSE050)

References: Networkx documentation https://networkx.org/documentation/stable/reference/index.html
            Stack overflow (for some unexpected errors)
"""

import networkx as nx
import csv
import gzip
import requests
import os

N = 25000


def DFSCycle(Graph, u, p, color: list,
             mark: list, par: list):
    global cyclenumber

    if color[u] == 2:
        return

    if color[u] == 1:
        cyclenumber += 1
        cur = p
        mark[cur] = cyclenumber

        while cur != u:
            cur = par[cur]
            mark[cur] = cyclenumber

        return

    par[u] = p

    color[u] = 1

    for v in Graph[u]:

        if v == par[u]:
            continue
        DFSCycle(Graph, v, u, color, mark, par)

    color[u] = 2


def getCycles(G):
    # basis = nx.cycle_basis(G)
    Graph = [[] for i in range(N)]
    cycles_list = [[] for i in range(N)]
    Graph.append([])

    for index, node in enumerate(G.nodes):
        Graph[index] = list(map(int, G.neighbors(node)))

    for i in range(N-len(Graph)):
        Graph.append([])

    color = [0] * N
    par = [0] * N
    mark = [0] * N

    DFSCycle(Graph, 1, 0, color, mark, par)

    for i in range(1, len(G.edges) + 1):
        if mark[i] != 0:
            cycles_list[mark[i]].append(i)

    cycles_list = list(filter(([]).__ne__, cycles_list))

    print(cycles_list)
    return cycles_list


def countBalandUnbal(G):
    count_bal = 0
    count_unbal = 0
    # H = G.to_directed()
    # cycles_list = list(nx.simple_cycles(H))
    cycles_list = getCycles(G)

    for cycle in cycles_list:
        curr_sign = 1
        pairs = [(a, b) for idx, a in enumerate(cycle)
                 for b in cycle[idx + 1:]]

        for pair in pairs:
            if pair in G.edges():
                sign = G[pair[0]][pair[1]]['weight']
                curr_sign *= sign

        if curr_sign < 0:
            count_unbal += 1
        elif curr_sign > 0:
            count_bal += 1

    print("Balanced cycles: ", count_bal)
    print("Unbalanced cycles: ", count_unbal)


def printedges(G):
    for edge in G.edges(data=True):
        print(edge)


def convertGraph(G):
    """
    Converting weighted signed to unweighted signed by putting
    -1 for weight<0 and +1 for weight>0.
    """
    for (u, v, w) in G.edges(data=True):
        if w['weight'] < 0:
            G.add_edge(u, v, weight=-1)

        if w['weight'] > 0:
            G.add_edge(u, v, weight=+1)

    countBalandUnbal(G)


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

    G = nx.Graph()

    # Creating graph
    with gzip.open('soc-sign-bitcoinalpha.csv.gz', 'rt') as file1:
        reader = csv.reader(file1)
        for row in reader:
            if row[0] not in G.nodes:
                G.add_node(row[0])
            if row[1] not in G.nodes:
                G.add_node(row[1])

            if (row[0], row[1]) and (row[1], row[0]) not in G.edges:
                G.add_edge(row[0], row[1], weight=int(row[2]))

    # Calling network measures functions
    G = nx.convert_node_labels_to_integers(G)
    convertGraph(G)

    # Remove downloaded file
    os.remove(Filename)

    print("======================================================")
    print()


if __name__ == "__main__":
    cyclenumber = 0
    main()
