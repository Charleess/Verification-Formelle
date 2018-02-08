""" Tous les k-chemins """
from ..common import compute_all_paths, browse_graph

def test_all_k_paths(graph, k, tests):
    """ Test the criteria """
    all_possible_paths = compute_all_paths(graph, 1, limit=k) # Get all the paths of length k
    max_node = max(list(graph.nodes)) # End node, where the program ends
    possible_paths = [
        path for path in all_possible_paths if path[len(path) - 1] == max_node
    ] # All paths that finish on the end node

    # Remove impossible paths
    # THIS IS CUSTOM TO OUR PROGRAM AND NOT REPLICABLE, AS EXPLAINED IN THE SUBJECT
    impossible_paths = [[1, 3, 4, 5] + [7, 5] * i + [8] for i in range((k - 4) // 2 + 1)]
    impossible_paths += [[1, 2, 4, 5] + [7, 5] * i + [8] for i in range(2, (k - 4) // 2 + 1)]

    possible_paths = [path for path in possible_paths if path not in impossible_paths] # Effectively do the cleaning
    total = len(possible_paths)

    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        if path in possible_paths:
            possible_paths = [p for p in possible_paths if p != path] # Remove the path if it's ok
    
    return(possible_paths, total)

def critere_k_TC(graph, k, tests):
    """ Main """
    remaining_paths, total = test_all_k_paths(graph, k, tests)
    
    try:
        res = (1 - (len(remaining_paths) / total)) * 100 # Get the percentage
        return res, remaining_paths
    except ValueError:
        return None