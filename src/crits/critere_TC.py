""" Toutes les conditions """
from ..common import browse_graph_verbose, get_condition_values
from copy import copy

def elems_to_cover_TC(graph):
    """ Returns a list of the elements to cover for the criterion """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges

    conditions_to_test = [] # List for the conditions to test
    for i, j in decision_edges: # Fill the list
        conditions_to_test += [
            (i, j, cond, [False, False]) for cond in graph.adj[i][j]["dec"][0]
        ] # The format is (node1, node2, condition as a lambda, [evaluated as true?, evaluated as false?])
    
    return {(i, j): len([cond for cond in conditions_to_test if cond[0] == i and  cond[1] == j]) for i, j in decision_edges}

def test_all_conditions(graph, tests, conditions_to_test):
    """ Test the criteria """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges

    conditions_to_test_tuples = [] # List for the conditions to test
    for i, j in decision_edges: # Fill the list
        conditions_to_test_tuples += [
            (i, j, cond, [False, False]) for cond in graph.adj[i][j]["dec"][0]
        ] # The format is (node1, node2, condition as a lambda, [evaluated as true?, evaluated as false?])

    conditions_to_test_fix = [(i, j, cond, [copy(a) for a in l]) for i, j, cond, l in conditions_to_test_tuples] # For the stats

    for t in tests:
        # Run the test
        path_with_values = browse_graph_verbose(t, graph) # Get the path associated with the test (as dic!)
        for cond in conditions_to_test_tuples: # Does the path evaluate the condition ?
            if cond[0] in path_with_values.keys(): # The condition is in the path
                for e in path_with_values[cond[0]]: # Iterate on the values the variables can have on this node
                    if cond[2](e): # Condition was evaluated to true
                        cond[3][0] = True # Store this information
                    else: # Condition was evaluated to false
                        cond[3][1] = True # Store this information
                    if cond[3] == [True, True]: # The condition has been evaluated both at true and false at some point
                        conditions_to_test_tuples = [c for c in conditions_to_test_tuples if c != cond] # Remove it

    return(conditions_to_test_tuples, conditions_to_test_fix)

def critere_TC(graph, tests, conditions_to_test):
    """ Main """
    conditions_to_test, conditions_to_test_fix = test_all_conditions(graph, tests, conditions_to_test)

    try:
        res = (1 - len(conditions_to_test) / len(conditions_to_test_fix)) * 100
        return res, conditions_to_test # Stats
    except ValueError:
        return None
