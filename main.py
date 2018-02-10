""" Main entry point """
import math
import sys
import ast
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
parser.add_argument("-d", "--draw-graph", action="store_true", help="draw the graph associated with the program")
parser.add_argument("-t", "--test", action="store_true", help="enable criteria testing")
parser.add_argument("-tc", "--test-criteria", type=str, nargs="*", choices=["TA", "TD", "k-TC", "i-TB", "TDef", "TU", "TDU", "TC"], help="the criteria to test")
parser.add_argument("-ts", "--test-set", nargs="+" ,help="the test set, as a list of dicts, e.g. [{'x': 1}, ...]")
parser.add_argument("-g", "--generate", action="store_true", help="enable tests generation")
parser.add_argument("-gc", "--generate-criteria", nargs="*", choices=["TA", "TD", "k-TC", "i-TB", "TDef", "TU", "TDU", "TC"], help="the criteria to generate test-sets for")
parser.add_argument("-gr", "--generate-range", type=int, help="the range used to look for test sets")

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

def generate_tests(graph, critere, elems_to_cover, rang = 15, **kwargs):
    # To simplify, we will hardcode the variables names here.
    candidates = [{'x': i} for i in range(-rang, rang)] # Get candidates for the search
    elems_to_cover_critere = elems_to_cover[critere] # Elems that need to be covered by the tests

    # Transform the elements to cover to a simpler representation (path, list of indices...)
    if critere == "TC":
        elems_to_cover_critere = get_elems_to_cover_idx_TC(elems_to_cover_critere)
    elif critere == "TU":
        elems_to_cover_critere = get_elems_to_cover_idx_TU(elems_to_cover_critere)
    elif critere == "TDU":
        elems_to_cover_critere = get_elems_to_cover_paths(elems_to_cover_critere)

    if type(next(iter(elems_to_cover_critere))) == list:
        # This is a criterion dealing with unhashable lists, convert to string
        elems_to_cover_set = set("-".join([str(i) for i in path]) for path in elems_to_cover_critere)
    else:
        # This deals with nodes or tuples, hashable
        elems_to_cover_set = set(elems_to_cover_critere)

    test_set = []

    # Basically, this is a set cover problem
    total_non_covered = elems_to_cover_set # This is the current elements to cover

    while total_non_covered != set():
        best_candidate = candidates[0] # Initialize candidate
        best_cand = [best_candidate.copy()]  # Our implementation has drawbacks...
        _, non_covered = critere_switch(critere, **kwargs)(graph, best_cand, elems_to_cover[critere], **kwargs)
        if len(non_covered) == 0 or type(next(iter(non_covered))) == list:  # For criteria where we deal with paths
            best_non_covered_elems = set("-".join([str(i) for i in path]) for path in non_covered) # Initialize candidate
        else:  # For criterias where we deal with nodes
            best_non_covered_elems = set(non_covered)
        best_non_covered = len(set(best_non_covered_elems))


        for cand in candidates: # Find a better one

            temp_cand = [test.copy() for test in test_set + [cand]]
            _, non_covered = critere_switch(critere, **kwargs)(graph, temp_cand, elems_to_cover[critere], **kwargs)
            if len(non_covered) == 0 or type(next(iter(non_covered))) == list:  # For criteria where we deal with paths
                set_non_covered_elems = set(
                    "-".join([str(i) for i in path]) for path in non_covered)  # Initialize candidate
            else:  # For criterias where we deal with nodes
                set_non_covered_elems = set(non_covered)
            # We check whether the added best candidate reduces the size of elements to cover or not
            if len(set_non_covered_elems) < best_non_covered:
                best_candidate = cand
                best_non_covered_elems = set_non_covered_elems
                best_non_covered = len(best_non_covered_elems)

        if best_non_covered < len(total_non_covered):
            test_set.append(best_candidate) # Add this candidate if they are better (better union)
            total_non_covered = best_non_covered_elems
        else:
            break

    return test_set, len(total_non_covered)/len(elems_to_cover_critere)

if __name__ == "__main__":
    graph = create_graph() # Initialize the graph for the program 'prog_1'

    ####################
    # SCHEMAS DE PROGS #
    ####################
    if args.draw_graph:
        draw_graph(graph) # Draw the graph in a window

    ##################
    # Initialisation #
    ##################

    if args.test:
        print("Testing: ON")
        if args.test_criteria:
            print("Testing criteria: {}".format(args.test_criteria))
            criteria_to_test = args.test_criteria
        else:
            print("No criteria specified, testing all criteria")
            criteria_to_test = ["TA", "TD", "k-TC", "i-TB", "TDef", "TU", "TDU", "TC"]

        if args.test_set:
            test_set_list = [ast.literal_eval(elem) for elem in args.test_set]
            print("Test set is: {}".format(test_set_list))
        else: # Default to range(-15, 15)
            print("No test set specified, defaulting to range(-15, 15)")
            test_set_list = [{'x': i} for i in range(-15,15)]
    else:
        print("Testing: OFF")
    
    if args.generate:
        print("Generation: ON")
        if args.generate_criteria:
            print("Generation criteria: {}".format(args.generate_criteria))
            criteria_to_generate = args.generate_criteria
        else:
            print("No criteria specified, generating all criteria")
            criteria_to_generate = ["TA", "TD", "k-TC", "i-TB", "TDef", "TU", "TDU", "TC"]

        if args.generate_range:
            generate_range = args.generate_range
        else: # Default to range(-15, 15)
            print("No range specified, defaulting to 15")
            generate_range = 15
    else:
        print("Generation: OFF")


    elems_to_cover = {}

    ####################
    # CRITERES DE TEST #
    ####################

    print("Démarrage...")
    elems_to_cover["TA"] = set(elems_to_cover_TA(graph))
    elems_to_cover["TD"] = set(elems_to_cover_TD(graph))
    elems_to_cover["k-TC"] = elems_to_cover_k_TC(graph, k=10)
    elems_to_cover["i-TB"] = elems_to_cover_i_TB(graph, i=10)
    elems_to_cover["TDef"] = elems_to_cover_TDef(graph)
    elems_to_cover["TU"] = elems_to_cover_TU(graph)
    elems_to_cover["TDU"] = elems_to_cover_TDU(graph)
    elems_to_cover["TC"] = elems_to_cover_TC(graph)
    input("Press any key to continue...")

    # EXAMPLE TA
    if args.test and "TA" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TA(graph, tests, elems_to_cover["TA"])
        print("Critere TA: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE TD
    if args.test and "TD" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TD(graph, tests, elems_to_cover["TD"])
        print("Critere TD: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE k-TC
    if args.test and "k-TC" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_k_TC(graph, tests, elems_to_cover["k-TC"], k=10)
        print("Critere k-TC: {} % - Elements non couverts (Chemins): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE i-TB
    if args.test and "i-TB" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_i_TB(graph, tests, elems_to_cover["i-TB"], i=10)
        print("Critere i-TB: {} % - Elements non couverts (Chemins): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE TDef
    if args.test and "TDef" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TDef(graph, tests, elems_to_cover["TDef"])
        print("Critere TDef: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE TU
    if args.test and "TU" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TU(graph, tests, elems_to_cover["TU"])
        print("Critere TU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE TDU
    if args.test and "TDU" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TDU(graph, tests, elems_to_cover["TDU"])
        print("Critere TDU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

    # EXAMPLE TC
    if args.test and "TC" in criteria_to_test:
        tests = [copy(test) for test in test_set_list]
        percentage, non_covered_elems = critere_TC(graph, tests, elems_to_cover["TC"])
        print("Critere TC: {} % - Elements non couverts (Conditions): {}".format(
            percentage,
            non_covered_elems
        ))

    #######################
    # GENERATION DE TESTS #
    #######################

    if args.generate and "TA" in criteria_to_generate:
        a, perc_a = generate_tests(graph, "TA", elems_to_cover, generate_range)
        print("Un jeu de test pour TA est: {}".format(a))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_a) * 100)))

    if args.generate and "TD" in criteria_to_generate:
        b, perc_b = generate_tests(graph, "TD", elems_to_cover, generate_range)
        print("Un jeu de test pour TD est: {}".format(b))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_b) * 100)))

    if args.generate and "k-TC" in criteria_to_generate:
        c, perc_c = generate_tests(graph, "k-TC", elems_to_cover, generate_range, k=10)
        print("Un jeu de test pour k-TC est: {}".format(c))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_c) * 100)))

    if args.generate and "i-TB" in criteria_to_generate:
        d, perc_d = generate_tests(graph, "i-TB", elems_to_cover, generate_range, i=1)
        print("Un jeu de test pour i-TB est: {}".format(d))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_d) * 100)))

    if args.generate and "TDef" in criteria_to_generate:
        e, perc_e = generate_tests(graph, "TDef", elems_to_cover, generate_range)
        print("Un jeu de test pour TDef est: {}".format(e))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_e) * 100)))

    if args.generate and "TU" in criteria_to_generate:
        f, perc_f = generate_tests(graph, "TU", elems_to_cover, generate_range)
        print("Un jeu de test pour TU est: {}".format(f))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_f) * 100)))

    if args.generate and "TDU" in criteria_to_generate:
        g, perc_g = generate_tests(graph, "TDU", elems_to_cover, generate_range)
        print("Un jeu de test pour TDU est: {}".format(g))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_g) * 100)))

    if args.generate and "TC" in criteria_to_generate:
        h, perc_h = generate_tests(graph, "TC", elems_to_cover, generate_range)
        print("Un jeu de test pour TC est: {}".format(h))
        print("Le test permet de couvrir {}% des éléments.".format(math.floor((1 - perc_h) * 100)))
