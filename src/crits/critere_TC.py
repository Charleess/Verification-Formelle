""" Toutes les conditions """
from ..common import browse_graph_verbose, get_condition_values
from copy import copy

def elems_to_cover_TC(graph):
    """ Returns a list of the elements to cover for the criterion """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges

    conditions_to_test = [] # List for the conditions to test
    conditions_to_test_id = []
    for i, j in decision_edges: # Fill the list
        conditions_to_test += [
            (i, j, cond, [False, False], "Cond n°{}".format(str(k))) for k, cond in enumerate(graph.adj[i][j]["dec"][0])
        ] # The format is (node1, node2, condition as a lambda, [evaluated as true?, evaluated as false?], index of condition in edge)

    return conditions_to_test

# Simplify the list of elements to cover (storing only indices)
def get_elems_to_cover_idx_TC(conditions_to_test):
    conditions_to_test_idx = [[i, j, s] for i, j, c, l, s in conditions_to_test]
    return conditions_to_test_idx

# Puts the conditions tests back to False
def initialize_conditions(conditions_to_test_tuples):
    conds = conditions_to_test_tuples
    for i, c in enumerate(conds):
        conds[i] = c[0], c[1], c[2], [False, False], c[4]
    return(conds)


def test_all_conditions(graph, tests, conditions_to_test):
    """ Test the criteria """

    conditions_to_test_tuples = conditions_to_test
    conditions_to_test_tuples = initialize_conditions(conditions_to_test_tuples)

    conditions_to_test_fix = [(i, j, cond, [copy(a) for a in l], idx) for i, j, cond, l, idx in conditions_to_test_tuples] # For the stats

    conditions_to_test_idx = get_elems_to_cover_idx_TC(conditions_to_test_fix)
    conditions_to_test_idx_fix = conditions_to_test_idx

    for t in tests:
        # Run the test
        path_with_values = browse_graph_verbose(t, graph) # Get the path associated with the test (as dic!)
        for cond in conditions_to_test_tuples: # Does the path evaluate the condition ?
            if cond[0] in path_with_values.keys(): # The node of the condition is in the path
                for e in path_with_values[cond[0]]: # Iterate on the values the variables can have on this node
                    if cond[2](e): # Condition was evaluated to true
                        cond[3][0] = True # Store this information
                    else: # Condition was evaluated to false
                        cond[3][1] = True # Store this information
                    if cond[3] == [True, True]: # The condition has been evaluated both at true and false at some point
                        #conditions_to_test_tuples = [c for c in conditions_to_test_tuples if c != cond] # Remove it
                        conditions_to_test_idx = [[i, j, s] for i, j, s in conditions_to_test_idx if [i, j, s] != [cond[0], cond[1], cond[4]]]
    return(conditions_to_test_idx, conditions_to_test_idx_fix)

def critere_TC(graph, tests, conditions_to_test):
    """ Main """
    conditions_to_test, conditions_to_test_fix = test_all_conditions(graph, tests, conditions_to_test)

    try:
        res = (1 - len(conditions_to_test) / max(len(conditions_to_test_fix), 1)) * 100
        return res, conditions_to_test # Stats
    except ValueError:
        return None
