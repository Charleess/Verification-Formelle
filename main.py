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
parser.add_argument("-ra", "--run-all", action="store_true", help="Run all the tests")

args = parser.parse_args()

if __name__ == "__main__":
    graph = create_graph() # Initialize the graph for the program 'prog_1'
    #draw_graph(graph) # Draw the graph in a window

    ####################
    # CRITERES DE TEST #
    ####################
    if args.run_all:
        tests = [{'x': i} for i in range(-15,15)]
        print("Critere TA: {} %".format(math.floor(critere_TA(graph, tests))))

        tests = [{'x': i} for i in range(-15,15)]
        print("Critere TD: {} %".format(math.floor(critere_TD(graph, tests))))

        tests = [{'x': i} for i in range(-15,15)]
        print("Critere k-TC: {} %".format(math.floor(critere_k_TC(graph, 10, tests))))

        tests = [{'x': i} for i in range(-100,100)]
        print("Critere i-TB: {} %".format(math.floor(critere_i_TB(graph, 3, tests))))

        tests = [{'x': i} for i in range(-20, 20)]
        print("Critere TDef: {} %".format(math.floor(critere_TDef(graph, tests))))

        tests = [{'x': i} for i in range(-20, 20)]
        print("Critere TU: {} %".format(math.floor(critere_TU(graph, tests))))

        tests = [{'x': i} for i in range(-20, 20)]
        print("Critere TDU: {} %".format(math.floor(critere_TDU(graph, tests))))

        tests = [{'x': i} for i in range(-3, 3)]
        print("Critere TC: {} %".format(math.floor(critere_TC(graph, tests))))

    #######################
    # GENERATION DE TESTS #
    #######################

