""" Main entry point """
from src.prog_1 import create_graph, draw_graph
from src.criteres import *
from src.common import Def, Ref
import math


if __name__ == "__main__":
    graph = create_graph()
    #draw_graph(graph)

    dico_test_1 = {'x': 5}
    dico_test_2 = {'x': 4}
    dico_test_3 = {'x': - 3}
    dico_test_4 = {'x': - 1}

    #tests = [dico_test_1, dico_test_2, dico_test_3, dico_test_4]

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
