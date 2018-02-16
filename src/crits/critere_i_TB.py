""" Toutes les i-boucles """
import networkx as nx
from ..common import subfinder, browse_graph, is_i_loop, compute_all_loops, compute_all_paths

def elems_to_cover_i_TB(graph, i=1):
    """ Returns a list of the elements to cover for the criterion """
    max_node = max(list(graph.nodes)) # Max node of the tree to limit the search
    loops = compute_all_loops(graph) # Get all the loops in the tree, if any
    max_loop_size = max([0] + [len(loop) for loop in loops]) # Max loop size is used for the search limit
    all_possible_paths = compute_all_paths(graph, 1, limit=max_loop_size * i * len(loops) + max_node) # Overkill
    # We limit the search to the height of the tree + i iterations of the loops, overshooting
    possible_paths = [path for path in all_possible_paths if path[len(path) - 1] == max_node] # Paths that lead to termination
    possible_paths = [path for path in possible_paths if is_i_loop(path, loops, i)] # Remove the paths with more than i iterations

    # Remove impossible paths
    # THIS IS CUSTOM TO OUR PROGRAM AND NOT REPLICABLE, AS EXPLAINED IN THE SUBJECT
    impossible_paths = [[1, 3, 4, 5] + [7, 5] * k + [8] for k in range((2 * i + max_node - 4) // 2 + 1)]
    impossible_paths += [[1, 2, 4, 5] + [7, 5] * k + [8] for k in range(2, (2 * i + max_node - 4) // 2 + 1)]

    possible_paths = [path for path in possible_paths if path not in impossible_paths] # Effectively do the cleaning

    return possible_paths

def test_all_i_loops(graph, tests, elems_to_cover, i=1):
    """ Test the criteria """
    possible_paths = elems_to_cover
    total = len(possible_paths)

    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path of the test
        if path in possible_paths:
            possible_paths = [p for p in possible_paths if p != path] # Remove the path from the list

    return(possible_paths, total)

def critere_i_TB(graph, tests, elems_to_cover, i=1):
    """ Main """
    remaining_paths, total = test_all_i_loops(graph, tests, elems_to_cover, i) # Get the paths that were not ok

    try:
        res = (1 - (len(remaining_paths) / max(total, 1))) * 100 # Get the percentage
        return res, remaining_paths
    except ValueError:
        return None