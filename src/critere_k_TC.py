""" Toutes les k-chemins """

def compute_all_paths(graph, i, limit=100):
    """ Get all the possible paths """
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

def test_all_k_paths(graph, k, tests):
    """ Test the criteria """
    all_possible_paths = compute_all_paths(graph, 1, limit=k)
    max_node = max(list(graph.nodes))
    possible_paths = [path for path in all_possible_paths if path[len(path) - 1] == max_node]

    # Suppression des chemins impossibles
    impossible_paths = [[1, 3, 4, 5] + [7, 5] * i + [8] for i in range((k - 4) // 2 + 1)]
    impossible_paths += [[1, 2, 4, 5] + [7, 5] * i + [8] for i in range(2, (k - 4) // 2 + 1)]

    possible_paths = [path for path in possible_paths if path not in impossible_paths]

    for t in tests:
        # Run the test
        path = browse_graph(t, graph)
        if path in possible_paths:
            possible_paths = [p for p in possible_paths if p != path]
    print(possible_paths)
    return(possible_paths == [])


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

def critere_k_TC(graph, tests):
    """ Main """
    var = test_all_k_paths(graph, 10, tests)
    return var
