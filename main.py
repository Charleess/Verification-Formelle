""" Main entry point """
from src.prog_1 import create_graph, draw_graph
from src.critereTA import CritereTA


if __name__ == "__main__":
    graph = create_graph()

    dico_test_1 = {'x': 5}
    dico_test_2 = {'x': 4}
    dico_test_3 = {'x': - 3}
    dico_test_4 = {'x': - 1}
    tests = [dico_test_1, dico_test_2, dico_test_3, dico_test_4]
    
    CritereTA(graph, tests)
