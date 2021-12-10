"""
Social Network Analysis: Programming Assignment 1
Author: Saurabh Burewar (B18CSE050)
The report is submitted in PDF formatted by the name "B18CSE050_assignment1_report.pdf"

References: Networkx documentation https://networkx.org/documentation/stable/reference/index.html
            Mathinsight degree distribution https://mathinsight.org/degree_distribution
            Stack overflow (for some unexpected errors)
"""

import networkx as nx
import csv
import gzip
import math
import matplotlib.pyplot as plt
import os
import requests


def Node_count(G):
    """
    The length of the set of nodes returned by G.nodes gives 
    the number of nodes in the Graph G.
    """
    nodes = len(G.nodes)
    print("Number of nodes: ", nodes)


def Edge_count(G):
    """
    The length of the set of edges returned by G.edges gives 
    the number of edges in the Graph G.
    """
    edges = len(G.edges)
    print("Number of edges: ", edges)


def Avg_degree(G):
    """
    Average degree is the sum of degrees of all nodes divided 
    by the number of nodes in the graph. The for loop gives the 
    sum of degrees of all nodes.
    """
    sum = 0
    for node in G.nodes:
        sum += G.degree(node)

    avg = sum/len(G.nodes)
    print("Average Degree: ", avg)


def Degree_dist(G):
    """
    Since it is directed graph we have in-degree, out-degree and 
    total degree distribution. A list of degrees is created 
    which is plotted in a histogram. This is done for in-degree, 
    out-degree and total degree. All distributions are saved in PNG 
    format in the folder "B18CSE050_plots" in root.
    """
    if not os.path.isdir('B18CSE050_plots'):
        os.mkdir("B18CSE050_plots")
    in_degrees = []
    out_degrees = []
    degrees = []
    for node in G.nodes:
        in_degrees.append(G.in_degree(node))
        out_degrees.append(G.out_degree(node))
        degrees.append(G.degree(node))

    plt.hist(in_degrees)
    plt.savefig("B18CSE050_plots/in_degree_dist.png")
    plt.hist(out_degrees)
    plt.savefig("B18CSE050_plots/out_degree_dist.png")
    plt.hist(degrees)
    plt.savefig("B18CSE050_plots/total_degree_dist.png")
    plt.show()
    print()
    print('Distributions saved in the folder "./B18CSE050_plots"')


def no_of_triangles(G):
    """
    Traingles are counted by taking an undirected instance of the 
    graph. nx.triangles() gives a dictionary with triangles for each 
    node. Since a triangle is counted 3 times in each node, the sum 
    gives 3 times the number of triangles in the graph. So, we divide 
    by 3 to get the number of triangles.
    """
    tri = nx.triangles(G.to_undirected())
    notri = sum(tri.values())//3
    print("Number of triangles: ", notri)


def diameter(G):
    """
    nx.diameter() gives diameter of graph but if graph is weakly 
    connected then it gives exception since diameter goes to 
    infinity. This exception is caught and diameter is shown as 
    infinity.
    """
    try:
        nx.diameter(G)
    except nx.exception.NetworkXError:
        print("Diameter: ", float(math.inf))


def Number_components(G):
    """
    Gives the number of components in the graph. Graph is seen as 
    undirected to count the components.
    """
    print("Number of components: ",
          nx.number_connected_components(G.to_undirected()))


def largest_component(G):
    """
    nx.connected components gives the set of nodes in each 
    component. The length of these sets gives the size of those 
    components. So, comp_list is a list of size of every component. 
    The max of this list gives sizze of largest component.
    """
    comp_list = []
    for c in nx.connected_components(G.to_undirected()):
        comp_list.append(len(c))

    print("Size of largest component: ", max(comp_list))
    print("Sizes of components: ", comp_list)


def clustering_coef(G):
    """
    nx.average_clustering gives the clustering coefficient of the 
    graph G.
    """
    print("Clustering coefficient: ", nx.average_clustering(G))


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
    Node_count(G)
    Edge_count(G)
    Avg_degree(G)
    no_of_triangles(G)
    diameter(G)
    Number_components(G)
    largest_component(G)
    clustering_coef(G)
    Degree_dist(G)

    # Remove downloaded file
    os.remove(Filename)

    # Drawing the network
    print()
    print("We are now drawing the graph. This might take a while.")
    print("If you do not want to wait, you can interrupt this program using 'Ctrl+C'")
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos, node_size=10, with_labels=False)
    plt.savefig("B18CSE050_plots/Graph.png")
    print()
    print('Graph saved in the folder "./B18CSE050_plots"')

    print("======================================================")
    print()


if __name__ == "__main__":
    main()
