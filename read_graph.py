
import networkx as nx
import numpy as np
from netwulf import visualize

numberOfNodes = -1
edges = []

# with open("data/jean.col") as file_in:
with open("data/inithx.i.3.col") as file_in:
    for line in file_in:
        arr = line.split()
        if arr[0] == 'p':
            numberOfNodes = int(arr[2])
        else:
            if arr[0] == 'e':
                edges.append((int(arr[1]), int(arr[2])))

#print(numberOfNodes)
#print(edges)

# Create a graph
G = nx.Graph()
nodes = [i for i in range(1,numberOfNodes+1)]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

visualize(G)
