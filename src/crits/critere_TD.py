""" Toutes les décisions """
from ..common import browse_graph, subfinder

def elems_to_cover_TD(graph):
    """ Returns a list of the elements to cover for the criterion """
    decision_edges = [
        (i, j) for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'if'
    ] # Get all the decision edges

    return decision_edges

def test_all_decisions(graph, tests, elems_to_cover):
    """ Test the criteria """
    decision_edges = elems_to_cover
    decision_edges_fix = decision_edges # For the stats

    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        for i, j in decision_edges:
            if subfinder(path, [i, j]): # Can we find the edge in the path ?
                decision_edges = [(k, l) for k, l in decision_edges if (k, l) != (i, j)] # Remove the node if it's ok

    return(decision_edges, decision_edges_fix)

def critere_TD(graph, tests, elems_to_cover):
    """ Main """
    decision_edges, decision_edges_fix = test_all_decisions(graph, tests, elems_to_cover)

    try:
        res = (1 - len(decision_edges) / len(decision_edges_fix)) * 100
        return res, decision_edges # Stats
    except ValueError:
        return None