import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms.community import label_propagation_communities
from sklearn.metrics import normalized_mutual_info_score
from itertools import islice
import numpy as np
import random


def lp_imp(G, itr):
    for node in G:
        G.nodes[node]['com_imp'] = 0

    for i in range(itr):

        A = nx.to_numpy_array(G)
        I = np.identity(len(G.nodes))
        S = np.add(A, I)
        S = np.linalg.matrix_power(np.add(A, I), 4)

        ks = nx.core_number(G)
        h = {}

        for node in G.nodes:
            eq = []
            for neighbor in G.neighbors(node):
                jac = nx.jaccard_coefficient(G, [(node, neighbor)])
                ks_neighbor = ks[neighbor]
                for u, v, p in jac:
                    eq.append(ks_neighbor*p)

            h[node] = S[node][node] * ks[node] * sum(eq)

        index = 0
        h_copy = h.copy()

        while h_copy:
            max_key = max(h_copy, key=lambda x: h_copy[x])
            max_neigh = max_key
            for neighbor in G.neighbors(max_key):
                if h[neighbor] > h[max_neigh]:
                    max_neigh = neighbor

            if h[max_neigh] > h[max_key]:
                G.nodes[max_key]['com_imp'] = G.nodes[neighbor]['com_imp']
            else:
                G.nodes[max_key]['com_imp'] = index
                index += 1

            h_copy.pop(max_key)

            # if neighbor not in h:
            #     G.nodes[max_key]['com_imp'] = G.nodes[neighbor]['com_imp']
            # else:
            #     G.nodes[max_key]['com_imp'] = index
            #     index += 1


def main():
    n = random.randint(1000, 2000)
    tau1 = 2
    tau2 = 1.1
    mu = 0.1
    G = nx.LFR_benchmark_graph(
        n, tau1, tau2, mu, min_degree=20, max_degree=50)

    G.remove_edges_from(nx.selfloop_edges(G))

    gt_comm = list({frozenset(G.nodes[node]['community']) for node in G})
    k = len(gt_comm)
    for index, c in enumerate(gt_comm):
        for node in list(c):
            G.nodes[node]['com_gt'] = index

    labels_gt = nx.get_node_attributes(G, 'com_gt')
    labels_gt = list(labels_gt.values())

    print("===================================================")
    print("            LP using Node Imp algorithm            ")
    print("---------------------------------------------------")
    lp_imp(G, 10)

    labels_imp = nx.get_node_attributes(G, 'com_imp')
    labels_imp = list(labels_imp.values())

    imp_nmi = normalized_mutual_info_score(labels_gt, labels_imp)
    print("NMI score for LP using Node Imp: ", imp_nmi)

    print("===================================================")
    print("            Label propagation algorithm            ")
    print("---------------------------------------------------")

    comps_lp = label_propagation_communities(G)
    for index, c in enumerate(comps_lp):
        for node in list(c):
            G.nodes[node]['com_lp'] = index

    labels_lp = nx.get_node_attributes(G, 'com_lp')
    labels_lp = list(labels_lp.values())

    lp_nmi = normalized_mutual_info_score(labels_gt, labels_lp)
    print("NMI score for Label propagation: ", lp_nmi)

    print("===================================================")
    print("              Girvan-Newman algorithm              ")
    print("---------------------------------------------------")
    print("This is going to take a long while......")

    comps_gn = girvan_newman(G)
    for communities in islice(comps_gn, k):
        com_tuple = tuple(sorted(c) for c in communities)

    for index, c in enumerate(com_tuple):
        for node in list(c):
            G.nodes[node]['com_gn'] = index

    labels_gn = nx.get_node_attributes(G, 'com_gn')
    labels_gn = list(labels_gn.values())

    gn_nmi = normalized_mutual_info_score(labels_gt, labels_gn)
    print("NMI score for Girvan-Newman: ", gn_nmi)

    print("===================================================")


if __name__ == "__main__":
    main()
