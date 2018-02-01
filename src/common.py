from inspect import getsource
import networkx as nx
import re

def subfinder(mylist, pattern):
    """ Little helper to find patterns in lists """
    matches = []
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            matches.append(pattern) # Add the pattern to the list
    return matches

def find_vars(graph, node):
    """ Returns the list of all the vars used on edges of type (node, child) """
    children = list(graph.successors(node)) # Our functions are defined on edges, not nodes
    if children != []:
        cond_vars = [] # Variables used in conditions
        cmd_vars_assign = [] # Variables defined of assigned
        cmd_vars_read = [] # Variables referenced for definition
        for child in children:
            code = getsource(graph.adj[node][child]["cmd"]) # Get the source code of the lambda function
            code_list = code.split("cond=")[1].strip().split("cmd=") # Parse the code to get the variable names
            cond_string, cmd_string = code_list

            cond_vars += [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cond_string)] # RegEx

            if re.findall(r"None", cmd_string) == ['None']:
                cmd_vars_assign_string, cmd_vars_read_string = cmd_string.split(":")
            else:
                cmd_vars_assign_string, cmd_vars_read_string = cmd_string.split(":")[1:]
            cmd_vars_assign += [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cmd_vars_assign_string)] # RegEx
            cmd_vars_read += [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cmd_vars_read_string)] # RegEx
        return [cond_vars, cmd_vars_assign, cmd_vars_read]

    else: # No definition or usage
        return [[], [], []]

def Ref(graph, node):
    """ Returns the list of all the vars REFFERED TO on edges of type (node, child) """
    cond_vars, cmd_vars_assign, cmd_vars_read = find_vars(graph, node)
    return list(set(cond_vars + cmd_vars_read))

def Def(graph, node):
    """ Returns the list of all the vars DEFINED on edges of type (node, child) """
    cond_vars, cmd_vars_assign, cmd_vars_read = find_vars(graph, node)
    return list(set(cmd_vars_assign))

def compute_all_loops(graph):
    """ Get all the possible loops """
    loops = list(nx.simple_cycles(graph))
    # As explained, this function is used for time saving, and could be reimplemented
    return loops

def compute_all_paths(graph, i, limit):
    """ Get all the possible paths """
    if limit < 0: # We reached the end of recursion
        return [[]]
    elif limit == 0: # We are at the end of the recursion, return the last node
        return [[i]]
    elif list(graph.successors(i)) == []:
        return [[i]] # This node has no successors, return it
    else:
        paths = []
        for k in graph.successors(i): # Iterate on every child
            paths_k = compute_all_paths(graph, k, limit=limit - 1)
            for path_k in paths_k:
                paths += [[i] + path_k] # Create paths by recursion, one layer at a time
        return paths

def is_i_loop(path, loops, i):
    """ Test if the path contains i iterations of each loop maximum """
    tst = []
    for loop in loops:
        tst.append(len(subfinder(path, loop))) # Append the max number of iterations of this loop

    correct = (max(tst) <= i) # Check if no loop is repeated more than i times

    return correct

def simple_paths(graph, u, v):
    """ Returns the simple paths aka with 1-loops """
    max_node = max(list(graph.nodes)) # Maximum node in the graph, for the limit
    loops = compute_all_loops(graph) # Get all the loops in the graph
    max_loop_size = max([len(loop) for loop in loops]) # Get the maximum loop size for the limit
    # Get all the paths starting from u, with maximum limit at 1 iteration per loop + the height of the graph
    all_possible_paths = compute_all_paths(graph, u, limit=max_loop_size * len(loops) + max_node)

    possible_paths = [path for path in all_possible_paths if path[len(path) - 1] == max_node]
    possible_paths = [path for path in possible_paths if is_i_loop(path, loops, 1)]

    # Cut the paths when they reach v
    result_paths = []
    for path in possible_paths:
        for index, char in enumerate(path):
            if char == v:
                result_paths.append(path[:index + 1]) # Only keep the beginning of the path
                break

    return [list(a) for a in list(set(tuple(path) for path in result_paths))]

def browse_graph(dico, graph):
    """ Execute the test in the dict and returns the path """
    tmp_node = 1 # Starting node
    path = [1] # Initial path
    while tmp_node != max(graph.nodes): # While we still have nodes to visit
        successors = list(graph.successors(tmp_node)) # Children
        i = 0
        not_found = True
        while not_found:
            v = successors[i] # Find successors of the node
            if graph.adj[tmp_node][v]['cond'](dico):
                graph.adj[tmp_node][v]['cmd'](dico) # Execute the command
                tmp_node = v # Switch node
                path += [v] # Update path
                not_found = False # Break out of the loop
            i += 1

    return (path)