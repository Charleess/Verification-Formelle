import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    G = nx.DiGraph()

    G.add_node(1)
    G.add_nodes_from([2,3,4,5,6,7])
    G.add_edge(1, 2, cond = lambda dic : dic['x']<=0, cmd = lambda dic : None, cmd_type = None)#vars = ['x']
    G.add_edge(1, 3, cond = lambda dic : not(dic['x']<=0), cmd = lambda dic : None, cmd_type = None)
    G.add_edge(2, 4, cond = lambda dic : True, cmd = lambda dic : dic.update({'x':-dic['x']}), cmd_type = 'assign')
    G.add_edge(3, 4, cond = lambda dic : True, cmd = lambda dic : dic.update({'x':1-dic['x']}), cmd_type = 'assign')
    G.add_edge(4, 5, cond = lambda dic : dic['x']==1, cmd = lambda dic : None, cmd_type = None)
    G.add_edge(4, 6, cond = lambda dic : not(dic['x']==1), cmd = lambda dic : None, cmd_type = None)
    G.add_edge(5, 7, cond = lambda dic : True, cmd = lambda dic : dic.update({'x':1}), cmd_type = 'assign')
    G.add_edge(6, 7, cond = lambda dic : True, cmd = lambda dic : dic.update({'x':1}), cmd_type = 'assign')

    return G


def draw_graph(G):
    layout = nx.spring_layout(G)
    nx.draw(G, with_labels=True, pos = layout)
    nx.draw_networkx_edge_labels(G, pos = layout)
    plt.show()