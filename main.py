""" Main entry point """
import math
from copy import copy
import argparse
from src.programs.prog_1 import create_graph, draw_graph
from src.crits.criteres import *

# Argument parser for the CLI
parser = argparse.ArgumentParser(
    prog="Structural Tester",
    description="Symbolic Execution Engine for Structural Testing"
)
parser.add_argument("-v", "--version", action="version", version="%(prog)s v1.0")
parser.add_argument("-ra", "--run-all", action="store_true", help="Run all the tests", default=True)

args = parser.parse_args()

def critere_switch(crit, **kwargs):
    """ Switch """
    return {
        "TA": lambda graph, test, critere_to_cover: critere_TA(graph, test, critere_to_cover),
        "TD": lambda graph, test, critere_to_cover: critere_TD(graph, test, critere_to_cover),
        "k-TC": lambda graph, test, critere_to_cover, **kwargs: critere_k_TC(graph, test, critere_to_cover, **kwargs),
        "i-TB": lambda graph, test, critere_to_cover, **kwargs: critere_i_TB(graph, test, critere_to_cover, **kwargs),
        "TDef": lambda graph, test, critere_to_cover: critere_TDef(graph, test, critere_to_cover),
        "TU": lambda graph, test, critere_to_cover: critere_TU(graph, test, critere_to_cover),
        "TDU": lambda graph, test, critere_to_cover: critere_TDU(graph, test, critere_to_cover),
        "TC": lambda graph, test, critere_to_cover: critere_TC(graph, test, critere_to_cover)
    }.get(crit)

def generate_tests(graph, critere, elems_to_cover, **kwargs):
    # To simplify, we will hardcode the variables names here.
    candidates = [{'x': i} for i in range(-10, 10)] # Get candidates for the search
    elems_to_cover_critere = elems_to_cover[critere] # Elems that need to be covered by the tests

    non_covered_elems = [] # We will get the non-covered itemps for each test
    for index, cand in enumerate(candidates): # Candidates are dictionnaries
        test_cand = {copy(key): copy(value) for key, value in cand.items()} # Our implementation has drawbacks...
        _, non_covered = critere_switch(critere, **kwargs)(graph, [test_cand], elems_to_cover[critere], **kwargs)

        if len(non_covered) == 0 or type(next(iter(non_covered))) == list: # For criteria where we deal with paths
            non_covered_elems.append(set("-".join([str(i) for i in path]) for path in non_covered))
        else: # For criterias where we deal with nodes
            non_covered_elems.append(non_covered)
    print(non_covered_elems)

    if type(next(iter(elems_to_cover_critere))) == list:
        # This is a criterion dealing with unhashable lists, convert to string
        elems_to_cover_set = set("-".join([str(i) for i in path]) for path in elems_to_cover_critere)
    else:
        # This deals with nodes or tuples, hashable
        elems_to_cover_set = set(elems_to_cover_critere)

    covered_elems = [
        elems_to_cover_set.difference(non_covered_elems[i]) for i in range(len(non_covered_elems))
    ] # Reverse the sets for a cleaner code. It's easier to deal with unions rather than intersections
    test_set = []

    # Basically, this is a set cover problem
    total_union = set() # This is the current conver
    while total_union != elems_to_cover_set:
        best_candidate_index = 0 # Initialize candidate
        best_candidate = candidates[0] # Initialize candidate
        best_covered = len(set(covered_elems[0])) # Initialize candidate
        for index, cand in enumerate(candidates): # Find a better one
            if len(set(covered_elems[index]).union(total_union)) > best_covered:
                best_candidate_index = index
                best_candidate = cand
                best_covered = len(set(covered_elems[index]).union(total_union))
        if len(set(covered_elems[best_candidate_index]).union(total_union)) > len(total_union):
            test_set.append(best_candidate) # Add this candidate if they are better (better union)
            total_union = set(covered_elems[best_candidate_index]).union(total_union)
        else:
            break

    return test_set

if __name__ == "__main__":
    graph = create_graph() # Initialize the graph for the program 'prog_1'
    #draw_graph(graph) # Draw the graph in a window

    elems_to_cover = {}

    ####################
    # CRITERES DE TEST #
    ####################
    if args.run_all:
        print("Démarrage...")

        # tests = [{'x': i} for i in range(-15,15)]
        # elems_to_cover["TA"] = set(elems_to_cover_TA(graph))
        # percentage, non_covered_elems = critere_TA(graph, tests, elems_to_cover["TA"])
        # print("Critere TA: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-15,15)]
        # elems_to_cover["TD"] = set(elems_to_cover_TD(graph))
        # percentage, non_covered_elems = critere_TD(graph, tests, elems_to_cover["TD"])
        # print("Critere TD: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-15,15)]
        # elems_to_cover["k-TC"] = elems_to_cover_k_TC(graph, k=10)
        # percentage, non_covered_elems = critere_k_TC(graph, tests, elems_to_cover["k-TC"], k=10)
        # print("Critere k-TC: {} % - Elements non couverts (Chemins): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-15,15)]
        # elems_to_cover["i-TB"] = elems_to_cover_i_TB(graph, i=10)
        # percentage, non_covered_elems = critere_i_TB(graph, tests, elems_to_cover["i-TB"], i=10)
        # print("Critere i-TB: {} % - Elements non couverts (Chemins): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-15, 15)]
        # elems_to_cover["TDef"] = elems_to_cover_TDef(graph)
        # percentage, non_covered_elems = critere_TDef(graph, tests, elems_to_cover["TDef"])
        # print("Critere TDef: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        tests = [{'x': i} for i in range(-15, 15)]
        elems_to_cover["TU"] = elems_to_cover_TU(graph)
        percentage, non_covered_elems = critere_TU(graph, tests, elems_to_cover["TU"])
        print("Critere TU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-20, 20)]
        elems_to_cover["TDU"] = elems_to_cover_TDU(graph)
        percentage, non_covered_elems = critere_TDU(graph, tests, elems_to_cover["TDU"])
        print("Critere TDU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        # tests = [{'x': i} for i in range(-3, 3)]
        # elems_to_cover["TC"] = elems_to_cover_TC(graph)
        # print(elems_to_cover["TC"])
        # percentage, non_covered_elems = critere_TC(graph, tests, elems_to_cover["TC"])
        # print("Critere TC: {} % - Elements non couverts (Conditions): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

    #######################
    # GENERATION DE TESTS #
    #######################

        # a = generate_tests(graph, "TA", elems_to_cover)
        # print("Un jeu de test pour TA est: {}".format(a))

        # b = generate_tests(graph, "TD", elems_to_cover)
        # print("Un jeu de test pour TD est: {}".format(b))

        # c = generate_tests(graph, "k-TC", elems_to_cover, k=10)
        # print("Un jeu de test pour k-TC est: {}".format(c))

        # d = generate_tests(graph, "i-TB", elems_to_cover, i=1)
        # print("Un jeu de test pour i-TB est: {}".format(d))

        # e = generate_tests(graph, "TDef", elems_to_cover)
        # print("Un jeu de test pour TDef est: {}".format(e))

        # g = generate_tests(graph, "TU", elems_to_cover)
        # print("Un jeu de test pour TU est: {}".format(g))

        # f = generate_tests(graph, "TDU", elems_to_cover)
        # print("Un jeu de test pour TDU est: {}".format(f))

        # h = generate_tests(graph, "TC", elems_to_cover)
        # print(h)