""" Toutes les conditions """
from ..common import browse_graph_verbose, get_condition_values
from copy import copy

def test_all_conditions(graph, tests):
    """ Test the criteria """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges

    conditions_to_test = [] # List for the conditions to test
    for i, j in decision_edges: # Fill the list
        conditions_to_test += [
            (i, cond, [False, False]) for cond in graph.adj[i][j]["dec"][0]
        ] # The format is (node, condition as a lambda, [evaluated as true?, evaluated as false?])
    conditions_to_test_fix = copy(conditions_to_test) # For the stats

    for t in tests:
        # Run the test
        path_with_values = browse_graph_verbose(t, graph) # Get the path associated with the test (as dic!)
        for cond in conditions_to_test: # Does the path evaluate the condition ?
            if cond[0] in path_with_values.keys(): # The condition is in the path
                for e in path_with_values[cond[0]]: # Iterate on the values the variables can have on this node
                    if cond[1](e): # Condition was evaluated to true
                        cond[2][0] = True # Store this information
                    else: # Condition was evaluated to false
                        cond[2][1] = True # Store this information
                    if cond[2] == [True, True]: # The condition has been evaluated both at true and false at some point
                        conditions_to_test = [c for c in conditions_to_test if c != cond] # Remove it

    return(conditions_to_test, conditions_to_test_fix)

def critere_TC(graph, tests):
    """ Main """
    conditions_to_test, conditions_to_test_fix = test_all_conditions(graph, tests)

    try:
        res = (1 - len(conditions_to_test) / len(conditions_to_test_fix)) * 100
        return res, conditions_to_test # Stats
    except ValueError:
        return None
