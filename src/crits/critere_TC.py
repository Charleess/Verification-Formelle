""" Toutes les conditions """
from ..common import browse_graph_verbose, get_condition_values
from copy import copy

def test_all_conditions(graph, tests):
    """ Test the criteria """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges
    decision_edges_fix = decision_edges # For the stats

    conditions_to_test = []
    for i, j in decision_edges:
        conditions_to_test += [(i, cond, [False, False]) for cond in graph.adj[i][j]["dec"][0]]
    conditions_to_test_fix = copy(conditions_to_test)

    for t in tests:
        # Run the test
        path_with_values = browse_graph_verbose(t, graph) # Get the path associated with the test (dic!)
        for cond in conditions_to_test:
            if cond[0] in path_with_values.keys():
                for e in path_with_values[cond[0]]: # Iterate on the values at this
                    if cond[1](e):
                        cond[2][0] = True
                    else:
                        cond[2][1] = True
                    if cond[2] == [True, True]:
                        conditions_to_test = [c for c in conditions_to_test if c != cond]

    return(conditions_to_test, conditions_to_test_fix)

def critere_TC(graph, tests):
    """ Main """
    conditions_to_test, conditions_to_test_fix = test_all_conditions(graph, tests)

    try:
        res = (1 - len(conditions_to_test) / len(conditions_to_test_fix)) * 100
        return res # Stats
    except ValueError:
        return None
