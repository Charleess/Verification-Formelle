import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    G = nx.DiGraph()

    G.add_edge(1, 2, cond=lambda dic: dic['x'] <= 0, cmd=lambda dic: None, cmd_type='if')
    G.add_edge(1, 3, cond=lambda dic: not(dic['x'] <= 0), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(2, 4, cond=lambda dic: True, cmd=lambda dic: dic.update({'x': - dic['x']}), cmd_type='assign')
    G.add_edge(3, 4, cond=lambda dic: True, cmd=lambda dic: dic.update({'x': 1 - dic['x']}), cmd_type='assign')
    G.add_edge(4, 5, cond=lambda dic: dic['x'] >= 1, cmd=lambda dic: None, cmd_type='if')
    G.add_edge(4, 6, cond=lambda dic: not(dic['x'] >= 1), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(5, 7, cond=lambda dic: True, cmd=lambda dic: dic.update({'x':1}), cmd_type='assign')
    G.add_edge(5, 7, cond=lambda dic: dic['x'] < 10, cmd=lambda dic: None, cmd_type='if')
    G.add_edge(7, 5, cond=lambda dic: True, cmd=lambda dic: dic.update({'x': dic['x'] + 1}), cmd_type='assign')
    G.add_edge(5, 8, cond=lambda dic: dic['x'] >= 10, cmd=lambda dic: None, cmd_type='if')
    G.add_edge(6, 8, cond=lambda dic: True, cmd=lambda dic: dic.update({'x': 1}), cmd_type='assign')

    return G


def draw_graph(graph):
    layout = nx.spring_layout(graph)
    nx.draw(graph, with_labels=True, pos = layout)
    #nx.draw_networkx_edge_labels(graph, pos = layout)
    plt.show()