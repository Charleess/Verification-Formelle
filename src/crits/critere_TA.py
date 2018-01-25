""" Toutes les affectations """

def test_all_affect(graph, tests):
    """ Test the criteria """
    assign_nodes_fix = [i for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'assign']
    assign_nodes = assign_nodes_fix
    for t in tests:
        # Run the test
        path = browse_graph(t, graph)
        for e in assign_nodes:
            if e in path:
                assign_nodes = [i for i in assign_nodes if i != e]

    return(assign_nodes, assign_nodes_fix)


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

def critere_TA(graph, tests):
    """ Main """
    assign_nodes, assign_nodes_fix = test_all_affect(graph, tests)

    try:
        res = (1 - len(assign_nodes) / len(assign_nodes_fix)) * 100
        return res
    except ValueError:
        return None
