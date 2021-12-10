import networkx as nx
import numpy as np
import random
from tqdm import tqdm


def icm(G, seed, p, itr, verbose=False):
    spread = 0

    for i in (tqdm(range(itr)) if verbose else range(itr)):
        active = seed[:]
        new = seed[:]

        while new:
            ongoing = []
            for curr in new:
                for neighbor in G.neighbors(curr):
                    randp = random.uniform(0, 1)
                    if randp < p:
                        if neighbor not in active:
                            ongoing.append(neighbor)

            new = list(set(ongoing) - set(active))
            active += new

        spread += len(active)

    spr = spread/itr
    return spr


def ltm(G, seed, itr, verbose=False):
    spread = 0

    for i in (tqdm(range(itr)) if verbose else range(itr)):
        active = seed[:]
        inactive = list(set(G.nodes) - set(active))

        while inactive:
            for curr in inactive:
                theta = random.random()
                b = []
                for neighbor in G.neighbors(curr):
                    b.append(random.random())

                if sum(b) >= theta:
                    active.append(curr)

                inactive.remove(curr)

        spread += len(active)

    spr = spread/itr
    return spr


def seed_select(G, k, p, itr, model):
    spreads = []
    sol = []

    for i in tqdm(range(k)):
        best_n = -1
        best_s = -np.inf

        nodes = set(range(len(G.nodes))) - set(sol)
        for node in nodes:
            if model == "icm":
                spread = icm(G, sol + [node], p, itr)
            elif model == "ltm":
                spread = ltm(G, sol + [node], p, itr)

            if spread > best_s:
                best_s = spread
                best_n = node

        sol.append(best_n)
        spreads.append(best_s)

    return sol, spreads


def ran_select(G, k, p, itr, model):
    ran_spreads = []
    ran_sol = []

    ran_seed = random.sample(G.nodes, k)
    for node in ran_seed:
        if model == "icm":
            spread = icm(G, ran_sol + [node], p, itr)
        elif model == "ltm":
            spread = ltm(G, ran_sol + [node], p, itr)

        ran_sol.append(node)
        ran_spreads.append(spread)

    return ran_sol, ran_spreads


def main():
    G = nx.barabasi_albert_graph(2000, 3)
    seed = random.sample(G.nodes, 50)

    print("==============================================")
    print("          Independent Cascade Model           ")
    print("----------------------------------------------")
    p = random.uniform(0.05, 0.15)
    spread_icm = icm(G, seed, p, 15000, True)
    print("Avg spread over iterations: ", spread_icm)

    print("==============================================")
    print("            Linear Threshold Model            ")
    print("----------------------------------------------")
    spread_ltm = ltm(G, seed, 15000, True)
    print("Avg spread over iterations: ", spread_ltm)

    print("==============================================")
    print("            Greedy seed selection             ")
    print("----------------------------------------------")
    sols, spreads = ran_select(G, 15, p, 10, "icm")
    print("Spreads of the 15 random nodes - \n", spreads)
    sols, spreads = seed_select(G, 15, p, 10, "icm")
    print("Spreads of the 15 best nodes - \n", spreads)

    print("==============================================")


if __name__ == "__main__":
    main()
