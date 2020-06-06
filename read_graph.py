# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# Graph import from file
import networkx as nx
from netwulf import visualize

files = ["graph-us-02.col", "queen7_7.col","jean.col", "le450_5a.col",]


class Graph:
    def __init__(self, num_of_nodes: int, edges_):
        self.nodes = [i for i in range(1, num_of_nodes + 1)]
        self.edges = edges_


def file_to_graph(file: str):
    num_of_nodes = -1
    edges = []
    path = "data/" + file
    with open(path) as file_in:
        for line in file_in:
            arr = line.split()
            if arr[0] == 'p':
                num_of_nodes = int(arr[2])
            else:
                if arr[0] == 'e':
                    edges.append((int(arr[1]), int(arr[2])))
    graph1 = Graph(num_of_nodes, edges)
    return graph1


# Create a graph
if __name__ == "__main__":
    G = nx.Graph()
    G_local = file_to_graph(files[0])
    G.add_nodes_from(G_local.nodes)
    G.add_edges_from(G_local.edges)

    visualize(G)
