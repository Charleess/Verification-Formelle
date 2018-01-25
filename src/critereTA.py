def test_all_affect(graph, tests):
    assign_nodes = [i for i, j in graph.edges if graph.adj[i][j]['cmd_type'] == 'assign']
    # for u, v in g.edges:
    #     if (g.adj[u][v]['cmd_type']=='Assign') and (u not in assign_nodes):
    #         assign_nodes += [u]
    for t in tests :
        path = browse_graph(t, graph)
        for e in assign_nodes:
            if e in path:
                assign_nodes = [i for i in assign_nodes if i != e]

    return(assign_nodes == [])


def browse_graph(dico, graph):
    tmp_node = 1
    path = [1]
    while tmp_node != max(graph.nodes):
        successors = list(graph.successors(tmp_node))
        i = 0
        not_found = True
        while not_found:
            v = successors[i]
            if graph.adj[tmp_node][v]['cond'](dico):
                graph.adj[tmp_node][v]['cmd'](dico)
                tmp_node = v
                path += [v]
                not_found = False
            i += 1

    return(path)

def CritereTA(graph, tests):
    var = test_all_affect(graph, tests)
    print(var)
