from src.common import Def, Ref
""" Toutes les definitions """

def test_all_definitions(graph, tests):
    """ Test the criteria """
    tests_paths = []
    for t in tests:
        # Run the test
        path = browse_graph(t, graph)
        tests_paths.append(path)

    def_node_list = [node for node in graph.nodes if Def(graph, node) != []]

    successes = []
    for node in def_node_list:
        def_var = Def(graph, node)[0]
        is_ref = False
        for path in tests_paths:
            #print(path)
            for i, n in enumerate(path):
                if n == node:
                    index = i
                    while (not is_ref) and (index < len(path) - 1):
                        index += 1
                        r = Ref(graph, path[index])
                        if def_var in r:
                            is_ref = True
        if is_ref:
            successes.append(node)
    print(def_node_list)
    print(successes)
    return(def_node_list, successes)


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

def critere_TDef(graph, tests):
    """ Main """
    def_node_list, successes = test_all_definitions(graph, tests)

    try:
        res = (len(successes) / len(def_node_list)) * 100
        return res
    except ValueError:
        return None
