""" Main entry point """
import math
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

if __name__ == "__main__":
    graph = create_graph() # Initialize the graph for the program 'prog_1'
    #draw_graph(graph) # Draw the graph in a window

    ####################
    # CRITERES DE TEST #
    ####################
    if args.run_all:
        print("Démarrage...")

        tests = [{'x': i} for i in range(-15,15)]
        percentage, non_covered_elems = critere_TA(graph, tests)
        print("Critere TA: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-15,15)]
        percentage, non_covered_elems = critere_TD(graph, tests)
        print("Critere TD: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-15,15)]
        percentage, non_covered_elems = critere_k_TC(graph, 10, tests)
        print("Critere k-TC: {} % - Elements non couverts (Chemins): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-100,100)]
        percentage, non_covered_elems = critere_i_TB(graph, 1, tests)
        print("Critere i-TB: {} % - Elements non couverts (Chemins): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-20, 20)]
        percentage, non_covered_elems = critere_TDef(graph, tests)
        print("Critere TDef: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-20, 20)]
        percentage, non_covered_elems = critere_TU(graph, tests)
        print("Critere TU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-20, 20)]
        percentage, non_covered_elems = critere_TDU(graph, tests)
        print("Critere TDU: {} % - Elements non couverts (Noeuds): {}".format(
            percentage,
            non_covered_elems
        ))

        tests = [{'x': i} for i in range(-3, 3)]
        percentage, non_covered_elems = critere_TC(graph, tests)
        print("Critere TC: {} % - Elements non couverts (Conditions): {}".format(
            percentage,
            non_covered_elems
        ))

    #######################
    # GENERATION DE TESTS #
    #######################

