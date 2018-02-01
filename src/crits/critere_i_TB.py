""" Toutes les i-boucles """
import networkx as nx
from ..common import subfinder

def compute_all_loops(graph):
    """ Get all the possible loops """
    loops = list(nx.simple_cycles(graph))
    # Returns a list of loops with no repetition
    return loops

def compute_all_paths(graph, i, limit):
    """ Get all the possible paths """
    # Recursive algorithm, iterate on all the children of a node, until the limit is reached
    # The limit prevents the infinite loops
    if limit < 0:
        return [[]]
    elif limit == 0:
        return [[i]]
    elif list(graph.successors(i)) == []:
        return [[i]]
    else:
        paths = []
        for k in graph.successors(i):
            paths_k = compute_all_paths(graph, k, limit=limit - 1)
            for path_k in paths_k:
                paths += [[i] + path_k]
        return paths

def is_i_loop(path, loops, i):
    """ Check whether a path contains i or less iterations of one of the loops """
    tst = [] # List of the sub-patterns
    for loop in loops:
        tst.append(len(subfinder(path, loop)))
    correct = (max(tst) <= i) # Check that no loop is repeated more than i times
    
    return correct # Boolean

def test_all_i_loops(graph, i, tests):
    """ Test the criteria """
    max_node = max(list(graph.nodes)) # Max node of the tree to limit the search
    loops = compute_all_loops(graph) # Get all the loops in the tree, if any
    max_loop_size = max([len(loop) for loop in loops]) # Max loop size is used for the search limit
    all_possible_paths = compute_all_paths(graph, 1, limit=max_loop_size * i * len(loops) + max_node) # Overkill
    # We limit the search to the height of the tree + i iterations of the loops, overshooting
    possible_paths = [path for path in all_possible_paths if path[len(path) - 1] == max_node] # Paths that lead to termination
    possible_paths = [path for path in possible_paths if is_i_loop(path, loops, i)] # Remove the paths with more than i iterations

    # Remove impossible paths
    # THIS IS CUSTOM TO OUR PROGRAM AND NOT REPLICABLE, AS EXPLAINED IN THE SUBJECT
    impossible_paths = [[1, 3, 4, 5] + [7, 5] * k + [8] for k in range((2 * i + max_node - 4) // 2 + 1)]
    impossible_paths += [[1, 2, 4, 5] + [7, 5] * k + [8] for k in range(2, (2 * i + max_node - 4) // 2 + 1)]

    possible_paths = [path for path in possible_paths if path not in impossible_paths] # Effectively do the cleaning
    total = len(possible_paths)

    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path of the test
        if path in possible_paths:
            possible_paths = [p for p in possible_paths if p != path] # Remove the path from the list

    return(possible_paths, total)


def browse_graph(dico, graph):
    """ Execute the test in the dict and returns the path """
    tmp_node = 1 # Starting node
    path = [1] # Initial path
    while tmp_node != max(graph.nodes):
        successors = list(graph.successors(tmp_node))
        i = 0
        not_found = True
        while not_found:
            v = successors[i] # Find successors of the node
            if graph.adj[tmp_node][v]['cond'](dico):
                graph.adj[tmp_node][v]['cmd'](dico) # Execute the command
                tmp_node = v
                path += [v]
                not_found = False
            i += 1

    return(path)

def critere_i_TB(graph, i, tests):
    """ Main """
    remaining_paths, total = test_all_i_loops(graph, i, tests) # Get the paths that were not ok

    try:
        res = (1 - (len(remaining_paths) / total)) * 100 # Get the percentage
        return res
    except ValueError:
        return None