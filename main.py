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

def critere_switch(crit, graph, test, critere_to_cover):
    """ Switch """
    return {
        "TA": critere_TA(graph, test, critere_to_cover)
    }.get(crit)

def generate_tests(graph, critere, elems_to_cover):
    # Update to get vars
    candidates = [{'x': i} for i in range(-10, 10)]
    elems_to_cover_critere = elems_to_cover[critere]

    non_covered_elems = []
    for index, cand in enumerate(candidates):
        test_cand = {copy(key): copy(value) for key, value in cand.items()}
        _, non_covered = critere_switch(critere, graph, [test_cand], elems_to_cover[critere])
        non_covered_elems.append(non_covered)

    elems_to_cover_set = set(elems_to_cover_critere)
    covered_elems = [elems_to_cover_set.difference(non_covered_elems[i]) for i in range(len(non_covered_elems))]
    test_set = []


    total_union = set()
    while total_union != elems_to_cover_set:
        best_candidate_index = 0
        best_candidate = candidates[0]
        best_covered = len(set(covered_elems[0]))
        for index, cand in enumerate(candidates):
            if len(set(covered_elems[index]).union(total_union)) > best_covered:
                best_candidate_index = index
                best_candidate = cand
                best_covered = len(set(covered_elems[index]).union(total_union))
        if len(set(covered_elems[best_candidate_index]).union(total_union)) > len(total_union):
            test_set.append(best_candidate)
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

        #tests = [{'x': i} for i in range(-15,15)]
        tests = [{'x': i} for i in [1, -2]]
        elems_to_cover["TA"] = set(elems_to_cover_TA(graph))
        percentage, non_covered_elems = critere_TA(graph, tests, elems_to_cover["TA"])
        print("Critere TA: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        a = generate_tests(graph, "TA", elems_to_cover)
        print(a)

        tests = [{'x': i} for i in range(-15,15)]
        elems_to_cover["TD"] = set(elems_to_cover_TD(graph))
        percentage, non_covered_elems = critere_TD(graph, tests)
        print("Critere TD: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        # tests = [{'x': i} for i in range(-15,15)]
        # percentage, non_covered_elems = critere_k_TC(graph, 10, tests)
        # print("Critere k-TC: {} % - Elements non couverts (Chemins): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-100,100)]
        # percentage, non_covered_elems = critere_i_TB(graph, 1, tests)
        # print("Critere i-TB: {} % - Elements non couverts (Chemins): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-20, 20)]
        # percentage, non_covered_elems = critere_TDef(graph, tests)
        # print("Critere TDef: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-20, 20)]
        # percentage, non_covered_elems = critere_TU(graph, tests)
        # print("Critere TU: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-20, 20)]
        # percentage, non_covered_elems = critere_TDU(graph, tests)
        # print("Critere TDU: {} % - Elements non couverts (Noeuds): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

        # tests = [{'x': i} for i in range(-3, 3)]
        # percentage, non_covered_elems = critere_TC(graph, tests)
        # print("Critere TC: {} % - Elements non couverts (Conditions): {}".format(
        #     percentage,
        #     non_covered_elems
        # ))

    #######################
    # GENERATION DE TESTS #
    #######################
