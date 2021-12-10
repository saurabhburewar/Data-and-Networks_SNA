import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import random
from tqdm import tqdm
import math


def random_combination(iterable, r):
    # This function is taken from python itertools documentation - recipes section
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


def lar_and_small_cliq(G):
    # This function is already something used in previous assignments
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

    print("     Largest clique - Size: ",
          max(cliq_len), ", Number: ", max_count)
    print("     Smallest clique - Size: ",
          min(cliq_len), ", Number: ", min_count)


def generate_many():
    print("Generating random graphs with different sizes...")
    for i in tqdm(range(100, 100000, 1000)):
        G = nx.erdos_renyi_graph(i, 0.5)
        degrees = [G.degree(node) for node in G.nodes]
        plt.hist(degrees, alpha=0.5)

    print("Generating scale-free graphs with different sizes...")
    for i in tqdm(range(100, 100000, 1000)):
        G = nx.barabasi_albert_graph(i, i-10)
        degrees = [G.degree(node) for node in G.nodes]
        plt.hist(degrees, alpha=0.5)

    plt.show()


def generate_NL(n, l):
    V = set([v for v in range(n)])
    E = set()

    while len(E) < l:
        E.add(random_combination(V, 2))

    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    return G


def generate_NP(n, p):
    V = set([v for v in range(n)])
    E = set()
    for combination in combinations(V, 2):
        a = random.random()
        if a < p:
            E.add(combination)

    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    return G


def analysis(G_rn, G_sf):

    print("Random Network")
    print("     Number of nodes: ", len(G_rn.nodes))
    print("     Number of edges: ", len(G_rn.edges))
    print("     Number of components: ", nx.number_connected_components(G_rn))

    sum_rn = 0
    for node in G_rn.nodes:
        sum_rn += G_rn.degree(node)

    avg_rn = sum_rn/len(G_rn.nodes)
    print("     Average Degree: ", avg_rn)

    tri_rn = nx.triangles(G_rn)
    notri_rn = sum(tri_rn.values())//3
    print("     Number of triangles: ", notri_rn)

    try:
        print("     Diameter: ", nx.diameter(G_rn))
    except nx.exception.NetworkXError:
        print("     Diameter: ", float(math.inf))

    print("     Clustering coefficient: ", nx.average_clustering(G_rn))
    lar_and_small_cliq(G_rn)

    print("Scale-free network")
    print("     Number of nodes: ", len(G_sf.nodes))
    print("     Number of edges: ", len(G_sf.edges))
    print("     Number of components: ", nx.number_connected_components(G_sf))

    sum_sf = 0
    for node in G_sf.nodes:
        sum_sf += G_sf.degree(node)

    avg_sf = sum_sf/len(G_sf.nodes)
    print("     Average Degree: ", avg_sf)

    tri_sf = nx.triangles(G_sf)
    notri_sf = sum(tri_sf.values())//3
    print("     Number of triangles: ", notri_sf)

    try:
        print("     Diameter: ", nx.diameter(G_sf))
    except nx.exception.NetworkXError:
        print("     Diameter: ", float(math.inf))

    print("     Clustering coefficient: ", nx.average_clustering(G_sf))
    lar_and_small_cliq(G_sf)

    # Degree distribution
    degrees_rn = [G_rn.degree(node) for node in G_rn.nodes]
    degrees_sf = [G_sf.degree(node) for node in G_sf.nodes]
    plt.hist(degrees_rn, alpha=0.5, label='Random')
    plt.hist(degrees_sf, alpha=0.5, label='Scale-free')
    plt.legend(loc='upper right')
    plt.title('Degree distribution')
    print()
    print("Degree distributions plotted")
    plt.show()


def main():
    print("Generate network from (N, L) or (N, P)")
    print("Enter '1' for (N, L) and '2' for (N, P)")
    method = int(input("Answer: "))

    if method == 1:
        print("======================================================")
        print("              Random graph with N and L               ")
        print("------------------------------------------------------")
        n = int(input("Give number of nodes: "))
        l = int(input("Give number of edges: "))
        G = generate_NL(n, l)
        print("Graph generated with given N and L")

    elif method == 2:
        print("======================================================")
        print("              Random graph with N and P               ")
        print("------------------------------------------------------")
        n = int(input("Give number of nodes: "))
        p = float(input("Give p: "))
        G = generate_NP(n, p)
        print("Graph generated with given N and P")

    print("======================================================")
    print("                     Question 3                       ")
    print("------------------------------------------------------")
    G_rn = nx.erdos_renyi_graph(100, 0.5)
    G_sf = nx.barabasi_albert_graph(100, 90)
    analysis(G_rn, G_sf)

    print("======================================================")
    print("                     Question 2                       ")
    print("------------------------------------------------------")
    generate_many()

    print("======================================================")


if __name__ == "__main__":
    main()
