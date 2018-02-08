""" Helpers and Project-Wide functions used in the different modules """
import re
from inspect import getsource
from copy import copy
import networkx as nx

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
            code_list = code.split("dec=")[1].strip().split("cmd=") # Parse the code to get the variable names
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
            if get_decision(graph.adj[tmp_node][v]['dec'], dico):
                graph.adj[tmp_node][v]['cmd'](dico) # Execute the command
                tmp_node = v # Switch node
                path += [v] # Update path
                not_found = False # Break out of the loop
            i += 1

    return (path)

def get_decision(decision_tuple, dico):
    """
    Get the decision from the conditions 
    decision_tuple = 
    ([
        lambda dic: dic['x'] >= 1,
        lambda dic: dic['y'] <= 2
    ], lambda a, b: a and b)
    """
    cond_outcome = []
    for e in decision_tuple[0]:
        cond_outcome.append(e(dico))
    
    if len(cond_outcome) == 0: # Lambda has to be evaluated on something
        cond_outcome = [True]

    result = decision_tuple[1](*cond_outcome)

    return result

def get_condition_values(decision_tuple, dico):
    """ Get the values for every condition """
    cond_outcome = []
    for e in decision_tuple[0]:
        cond_outcome.append(e(dico))

    return cond_outcome # Return a list of booleans corresponding to each condition

def shallow_copy(dic):
    """ Returns a shallow copy of a dictionnary """
    res = {}
    for key in dic.keys():
        res[key] = copy(dic[key])
    return res

def browse_graph_verbose(dico, graph):
    """ Execute the test in the dict and returns the path + dic values """
    tmp_node = 1 # Starting node
    path = {1: [shallow_copy(dico)]} # Initial path
    while tmp_node != max(graph.nodes): # While we still have nodes to visit
        successors = list(graph.successors(tmp_node)) # Children
        i = 0
        not_found = True
        while not_found:
            v = successors[i] # Find successors of the node
            if get_decision(graph.adj[tmp_node][v]['dec'], dico):
                graph.adj[tmp_node][v]['cmd'](dico) # Execute the command
                tmp_node = v # Switch node
                try:
                    path[v].append(shallow_copy(dico)) # Update path
                except KeyError:
                    path[v] = [shallow_copy(dico)]
                not_found = False # Break out of the loop
            i += 1

    return (path)
