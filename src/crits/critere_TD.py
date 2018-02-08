""" Toutes les décisions """
from ..common import browse_graph

def test_all_decisions(graph, tests):
    """ Test the criteria """
    decision_nodes = [
        i for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision nodes
    decision_nodes_fix = decision_nodes # For the stats
    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        for e in decision_nodes:
            if e in path:
                decision_nodes = [i for i in decision_nodes if i != e] # Remove the node if it's ok

    return(decision_nodes, decision_nodes_fix)

def critere_TD(graph, tests):
    """ Main """
    decision_nodes, decision_nodes_fix = test_all_decisions(graph, tests)

    try:
        res = (1 - len(decision_nodes) / len(decision_nodes_fix)) * 100
        return res # Stats
    except ValueError:
        return None