""" Toutes les affectations """
from ..common import browse_graph

def test_all_affect(graph, tests):
    """ Test the criteria """
    assign_nodes_fix = [i for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'assign'] # Get all the assign nodes
    assign_nodes = assign_nodes_fix # Duplicate for the stats
    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        for e in assign_nodes:
            if e in path:
                assign_nodes = [i for i in assign_nodes if i != e] # Remove the nodes that satisfie the criterion

    return(assign_nodes, assign_nodes_fix)

def critere_TA(graph, tests):
    """ Main """
    assign_nodes, assign_nodes_fix = test_all_affect(graph, tests)

    try:
        res = (1 - len(assign_nodes) / len(assign_nodes_fix)) * 100
        return res # Stats
    except ValueError:
        return None
