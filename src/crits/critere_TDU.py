from src.common import Def, Ref, simple_paths, browse_graph, subfinder
""" Toutes les utilisations """

def elems_to_cover_TDU(graph):
    """ Returns a list of the elements to cover for the criterion """
    def_nodes_list = [
        node for node in graph.nodes if Def(graph, node) != []
    ] # All the definition nodes

    ref_node_list = [node for node in graph.nodes if Ref(graph, node) != []] # All the reference nodes

    possible_paths_dico = {} # Holds the state of the test run

    for node in def_nodes_list: # For every definition ...
        possible_paths_dico[node] = {}
        def_var = Def(graph, node)[0] # The defined variable, there can be only one
        ref_nodes = [n for n in ref_node_list if def_var in Ref(graph, n)] # All the nodes that refer to this variable

        for ref_node in ref_nodes:
            possible_paths_dico[node][ref_node] = [] # Paths from u to ref_node
            possible_paths = simple_paths(graph, node, ref_node) # Get all the simple paths from u to ref_node

            for path in possible_paths:
                is_valid = True
                for e in path[1:-1]:
                    if def_var in Def(graph, e): # We redefine the variable, the path is not correct
                        is_valid = False
                if is_valid:
                    possible_paths_dico[node][ref_node].append(path) # This path is ok
            # Now we have all the paths that go from u to v and do not redefine the variable defined in u
            if possible_paths_dico[node][ref_node] == [] or possible_paths_dico[node][ref_node] == [[node]]:
                possible_paths_dico[node].pop(ref_node)
    return possible_paths_dico

def get_elems_to_cover_paths(possible_paths_dico):
    elems_paths = []
    for u in possible_paths_dico.keys():
        for v in possible_paths_dico[u].keys():
            for path in possible_paths_dico[u][v]:
                elems_paths.append(path)
    return elems_paths

def test_all_usages_paths(graph, tests, elems_to_cover):
    """ Test the criteria """
    tests_paths = []
    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        tests_paths.append(path)

    possible_paths_dico = elems_to_cover
    paths_to_cover = get_elems_to_cover_paths(possible_paths_dico)
    paths_to_cover_fix = paths_to_cover

    for path in paths_to_cover_fix:
        for test_path in tests_paths:
            if len(subfinder(test_path, path)) > 0:  # The path was found in at least one of the tests
                paths_to_cover = [p for p in paths_to_cover if p != path]

    return(paths_to_cover_fix, paths_to_cover)

def critere_TDU(graph, tests, elems_to_cover):
    """ Main """
    paths_to_cover_fix, paths_to_cover = test_all_usages_paths(graph, tests, elems_to_cover)
    try:
        res = (1 - len(paths_to_cover) / max(1, len(paths_to_cover_fix))) * 100
        return res, paths_to_cover
    except ValueError:
        return None
