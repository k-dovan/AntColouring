# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# Ant colony algorithm implementation
from read_graph import Graph
from random import randint
import networkx as nx
from netwulf import visualize


# random_graph_generator(...) - graph with random edges generator
def random_graph_generator(num_of_nodes: int, num_of_edges):
    if num_of_nodes <= 0:
        raise Exception('Number of nodes must be bigger than 0')
    max_edges = num_of_nodes * (num_of_nodes - 1)/2
    if num_of_edges > max_edges:
        raise Exception('Too many edges')
    edges = []
    while len(edges) < num_of_edges:
        new_edge = (randint(1, num_of_nodes), randint(1, num_of_nodes))
        opposite_edge = (new_edge[1], new_edge[0])
        if new_edge[0] == new_edge[1]:
            continue
        if new_edge not in edges and opposite_edge not in edges:
            edges.append(new_edge)
    return Graph(num_of_nodes, edges)


# bipartite_graph_generator(...) - bipartite graph with random edges generator
def bipartite_graph_generator(num_of_nodes_1: int, num_of_nodes_2: int, num_of_edges: int):
    if num_of_nodes_1 <= 0 or num_of_nodes_2 <= 0:
        raise Exception('Number of nodes must be bigger than 0')
    max_edges = num_of_nodes_1 * num_of_nodes_2
    if num_of_edges > max_edges:
        raise Exception('Too many edges')
    edges = []
    while len(edges) < num_of_edges:
        new_edge = (randint(1, num_of_nodes_1), randint(num_of_nodes_1 + 1, num_of_nodes_1 + num_of_nodes_2))
        if new_edge not in edges:
            edges.append(new_edge)
    return Graph(num_of_nodes_1 + num_of_nodes_2, edges)


def complete_graph_generator(num_of_nodes: int):
    if num_of_nodes <= 0:
        raise Exception('Number of nodes must be bigger than 0')
    edges = []
    for i in range(1, num_of_nodes+1):
        if i < num_of_nodes:
            for j in range(i + 1, num_of_nodes + 1):
                edges.append((i, j))
    return Graph(num_of_nodes, edges)


# one_vert_connected_graph_generator(...) - graph contains two complete graphs connected through one additional node
def one_vert_connected_graph_generator(num_of_nodes_1: int, num_of_nodes_2: int):
    if num_of_nodes_1 <= 0 or num_of_nodes_2 <= 0:
        raise Exception('Number of nodes must be bigger than 0')
    connected1 = complete_graph_generator(num_of_nodes_1)
    connected2 = complete_graph_generator(num_of_nodes_2)
    edges_part2 = [(edge[0] + num_of_nodes_1, edge[1] + num_of_nodes_1) for edge in connected2.edges]
    additional_edge_1 = (num_of_nodes_1 + num_of_nodes_2 + 1, randint(1, num_of_nodes_1))
    additional_edge_2 = (num_of_nodes_1 + num_of_nodes_2 + 1, randint(num_of_nodes_1 + 1, num_of_nodes_1 + num_of_nodes_2))
    edges = connected1.edges + edges_part2 + [additional_edge_1] + [additional_edge_2]
    one_vert_connected_graph = Graph(num_of_nodes_1 + num_of_nodes_2 + 1, edges)
    return one_vert_connected_graph


def graph_to_file(graph: Graph, file_name: str):
    num_of_nodes = len(graph.nodes)
    num_of_edges = len(graph.edges)
    with open('data/' + file_name + '.col', 'w') as file:
        file.write('p edge ' + str(num_of_nodes) + ' ' + str(num_of_edges) + '\n')
        for edge in graph.edges:
            file.write('e ' + str(edge[0]) + ' ' + str(edge[1]) + '\n')
        file.close()


if __name__ == "__main__":
    graph = random_graph_generator(5, 6)
    graph2 = bipartite_graph_generator(3, 4, 12)
    graph3= complete_graph_generator(4)
    graph4 = one_vert_connected_graph_generator(14, 7)
    G = nx.Graph()
    G.add_nodes_from(graph4.nodes)
    G.add_edges_from(graph4.edges)

    # graph_to_file(graph4, 'experiment1')

    visualize(G)