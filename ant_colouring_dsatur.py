
import networkx as nx
import numpy as np
from netwulf import visualize

# global variables
G = None                    # networkX graph instance

# read a graph from a text file
# param filename - fullname of the file contains graph data
def create_graph_from_file(filename):
    edges = []
    with open(filename) as file_in:
        for line in file_in:
            arr = line.split()
            if arr[0] == 'p':
                number_of_nodes = int(arr[2])
            else:
                if arr[0] == 'e':
                    edges.append((int(arr[1]), int(arr[2])))
    global G
    G = nx.Graph()
    nodes = [i for i in range(1, number_of_nodes + 1)]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

# visualize graph using netwulf
def visualize_graph():
    global G
    visualize(G)



if __name__ == "__main__":
    filename = "data/inithx.i.3.col"
    create_graph_from_file(filename)
    # visualize_graph()
