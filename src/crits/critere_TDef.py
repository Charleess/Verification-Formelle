""" Toutes les definitions """
from src.common import Def, Ref, browse_graph

def test_all_definitions(graph, tests):
    """ Test the criteria """
    tests_paths = [] # List of all the paths associated with the tests
    for t in tests:
        # Run the test
        path = browse_graph(t, graph) # Get the path associated with the test
        tests_paths.append(path)

    def_node_list = [
        node for node in graph.nodes if Def(graph, node) != []
    ] # All the nodes that define something

    successes = []
    for node in def_node_list: # This node defines a variable
        def_var = Def(graph, node)[0] # Varible defined by the node
        
        is_ref = False # Is the variable referenced ?
        for path in tests_paths:
            for i, n in enumerate(path): # Go along the path
                if n == node:
                    index = i # We stopped on the defining node, will the ref occur ?
                    while (not is_ref) and (index < len(path) - 1):
                        index += 1 # Continue on the path
                        r = Ref(graph, path[index])
                        if def_var in r: # The variable has been ref'd
                            is_ref = True # Set it ok
        if is_ref:
            successes.append(node) # This node is ok

    return(def_node_list, successes)

def critere_TDef(graph, tests):
    """ Main """
    def_node_list, successes = test_all_definitions(graph, tests)

    try:
        res = (len(successes) / len(def_node_list)) * 100
        return res, list(set(def_node_list) - set(successes)) # Statistic
    except ValueError:
        return None
