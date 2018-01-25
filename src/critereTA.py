def test_all_affect(graph, tests):
    """ Test the criteria """
    assign_nodes = [i for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'assign']
    for t in tests:
        # Run the test
        path = browse_graph(t, graph)
        for e in assign_nodes:
            if e in path:
                assign_nodes = [i for i in assign_nodes if i != e]

    return(assign_nodes == [])


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

def CritereTA(graph, tests):
    var = test_all_affect(graph, tests)
    print(var)
