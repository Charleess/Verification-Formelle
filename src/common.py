from inspect import getsource
import re

def find_vars(graph, node):
    """ Returns the list of all the vars used on edges of type (node, child) """
    children = list(graph.successors(node))
    if children != []:
        child = children[0]
        code = getsource(graph.adj[node][child]["cmd"])
        code_list = code.split("cond=")[1].strip().split("cmd=")
        cond_string, cmd_string = code_list

        cond_vars = [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cond_string)]

        if re.findall(r"None", cmd_string) == ['None']:
            cmd_vars_assign_string, cmd_vars_read_string = cmd_string.split(":")
        else:
            cmd_vars_assign_string, cmd_vars_read_string = cmd_string.split(":")[1:]
        cmd_vars_assign = [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cmd_vars_assign_string)]
        cmd_vars_read = [var.replace("'", "") for var in re.findall(r"\'[A-Za-z0-9]\'+", cmd_vars_read_string)]
        return [cond_vars, cmd_vars_assign, cmd_vars_read]

    else:
        return [[], [], []]

def Ref(graph, node):
    """ Returns the list of all the vars DEFINED on edges of type (node, child) """
    cond_vars, cmd_vars_assign, cmd_vars_read = find_vars(graph, node)
    return list(set(cond_vars + cmd_vars_read))

def Def(graph, node):
    """ Returns the list of all the vars REFFERED TO on edges of type (node, child) """
    cond_vars, cmd_vars_assign, cmd_vars_read = find_vars(graph, node)
    return list(set(cmd_vars_assign))
