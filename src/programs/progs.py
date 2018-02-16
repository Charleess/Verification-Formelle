import networkx as nx
import matplotlib.pyplot as plt


def create_graph_1():
    G = nx.DiGraph()

    G.add_edge(1, 2, dec=([lambda dic: dic['x'] <= 0], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(1, 3, dec=([lambda dic: not(dic['x'] <= 0)], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(2, 4, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': - dic['x']}), cmd_type='assign')
    G.add_edge(3, 4, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': 1 - dic['x']}), cmd_type='assign')
    G.add_edge(4, 5, dec=([lambda dic: dic['x'] >= 1], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(4, 6, dec=([lambda dic: not(dic['x'] >= 1)], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(5, 7, dec=([lambda dic: dic['x'] < 3], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(7, 5, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': dic['x'] + 1}), cmd_type='assign')
    G.add_edge(5, 8, dec=([lambda dic: dic['x'] >= 3], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(6, 8, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': 1}), cmd_type='assign')

    return G

def create_graph_2():
    G = nx.DiGraph()

    G.add_edge(1, 2, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': -dic['x']}), cmd_type='assign')
    G.add_edge(2, 3, dec=([lambda dic: dic['x'] <= 0], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(2, 4, dec=([lambda dic: not(dic['x'] <= 0)], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(3, 7, dec=([], lambda a: True), cmd=lambda dic: dic.update({'y': - dic['y']}), cmd_type='assign')
    G.add_edge(4, 5, dec=([lambda dic: dic['x'] <= -1], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(4, 6, dec=([lambda dic: not (dic['x'] <= -1)], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(5, 7, dec=([], lambda a: True), cmd=lambda dic: dic.update({'y': 1 - dic['y']}), cmd_type='assign')
    G.add_edge(6, 7, dec=([], lambda a: True), cmd=lambda dic: dic.update({'y': 1}), cmd_type='assign')
    G.add_edge(7, 8, dec=([], lambda a: True), cmd=lambda dic: dic.update({'y': dic['x']}), cmd_type='assign')

    return G

def create_graph_3():
    G = nx.DiGraph()
    G.add_edge(1, 2, dec=([lambda dic: dic['x'] <= 0], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(1, 3, dec=([lambda dic: not (dic['x'] <= 0)], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(2, 4, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': dic['x']-3}), cmd_type='assign')
    G.add_edge(3, 4, dec=([], lambda a: True), cmd=lambda dic: None, cmd_type='skip')
    G.add_edge(4, 5, dec=([lambda dic: dic['x'] < 0], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(4, 6, dec=([lambda dic: not dic['x'] < 0], lambda a: a), cmd=lambda dic: None, cmd_type='if')
    G.add_edge(5, 4, dec=([], lambda a: True), cmd=lambda dic: dic.update({'x': dic['x'] + 1}), cmd_type='assign')
    return G

def draw_graph(graph):
    layout = nx.spring_layout(graph)
    nx.draw(graph, with_labels=True, pos = layout)
    #nx.draw_networkx_edge_labels(graph, pos = layout)
    plt.show()
