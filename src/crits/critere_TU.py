from src.common import Def, Ref, simple_paths, browse_graph, subfinder
""" Toutes les utilisations """

def test_all_usages(graph, tests):
    """ Test the criteria """
    tests_paths = []
    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        tests_paths.append(path)

    def_node_list = [node for node in graph.nodes if Def(graph, node) != []] # All the definition nodes
    ref_node_list = [node for node in graph.nodes if Ref(graph, node) != []] # All the reference nodes
    successes = []
    possible_paths_dico = {} # Holds the state of the test run

    for node in def_node_list: # For every definition ...
        possible_paths_dico[node] = {}
        def_var = Def(graph, node)[0] # The defined variable, there can be only one
        ref_nodes = [n for n in ref_node_list if Ref(graph, n) == def_var] # All the nodes that refer to this variable

        for ref_node in ref_nodes:
            possible_paths_dico[node][ref_node] = [] # Paths from u to ref_node
            possible_paths = simple_paths(graph, node, ref_node) # Get all the simple paths from u to ref_node

            for path in possible_paths:
                is_valid = True
                for e in path[1:-1]:
                    if def_var in Def(e): # We redefine the variable, the path is not correct
                        is_valid = False
                if is_valid:
                    possible_paths_dico[node][ref_node].append(path) # This path is ok
            # Now we have all the paths that go from u to v and do not redefine the variable defined in u

    for u in def_node_list: # We can now check the criterion
        all_ok = True
        for v in possible_paths_dico[u].keys():
            all_ok_v = False
            for subpath in possible_paths_dico[u][v]:
                for test_path in test_paths:
                    if len(subfinder(tests_path, subpath)) > 0: # The path was found in at least one of the tests
                        all_ok_v = True
            all_ok = all_ok and all_ok_v # AT LEAST and not FOR ALL
        if all_ok:
            successes.append(u)

    return(def_node_list, successes)

def critere_TU(graph, tests):
    """ Main """
    ref_node_list, successes = test_all_usages(graph, tests)

    try:
        res = (len(successes) / len(ref_node_list)) * 100
        return res
    except ValueError:
        return None
