
from read_graph import Graph, file_to_graph, files
import networkx as nx
from netwulf import visualize
import  netwulf as nw
import matplotlib.pyplot as plt
import pandas as pd
from random import randrange

def standardize_graph(graph: Graph):
    for e in graph.edges:
        opposite_edge = (int(e[1]), int(e[0]))
        if opposite_edge in graph.edges:
            graph.edges.remove(opposite_edge)
    return graph

# [Khanh3] visualize graph by netwulf
def visualizing_coloured_graph(graph: Graph, colours: []):
    # we first standardize the graph
    graph = standardize_graph(graph)
    # build networkx graph
    G = nx.Graph()
    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    colour_dict = pd.DataFrame({'node': graph.nodes, 'color': colours})
    colour_dict['color'] = pd.Categorical(colour_dict['color'])
    colour_code = colour_dict['color'].cat.codes

    # Custom the nodes:
    nx.draw(G, with_labels=True, node_color=colour_code, cmap=plt.cm.Set1, node_size=1500)

    plt.show()

# [Khanh3] visualize graph by netwulf
def visualizing_coloured_graph_by_netwulf(graph: Graph, colours: []):
    # we first standardize the graph
    graph = standardize_graph(graph)
    # build networkx graph
    G = nx.Graph()
    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    # add group for nodes
    for k, v in G.nodes(data=True):
        v['group'] = colours[k-1]

    network = visualize(G, config={'zoom':2.5,
                                   'display_node_labels': True,
                                   'link_distance': 30,
                                   'node_gravity': 0})

if __name__ == "__main__":

    graph = file_to_graph(files[0])

    colours = [randrange(5) for i in graph.nodes]

    # visualizing_coloured_graph(graph, colours)
    visualizing_coloured_graph_by_netwulf(graph,colours)