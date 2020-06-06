# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# Ant colony algorithm implementation
from DSATUR import dsatur, MTrail
from read_graph import Graph, file_to_graph, files
import numpy as np
from visualizing_graph import visualizing_coloured_graph, \
     visualizing_coloured_graph_by_netwulf


class BestSolution:
    def __init__(self):
        self.q = float('inf')
        self.colours = []


# [Kasia] check if graph is simple and make it directed
def is_simple_undirected(graph: Graph):
    for edge in graph.edges:
        if edge[0] == edge[1]:
            raise Exception('graph not simple')
        opposite_edge = (int(edge[1]), int(edge[0]))
        if opposite_edge not in graph.edges:
            # make graph directed
            graph.edges.append(opposite_edge)


def ant_colony(graph: Graph, n_ants=5, max_cycles=5, p_coeff=0.5, alpha=2, beta=4):
    is_simple_undirected(graph)
    # Variables
    num_of_nodes = len(graph.nodes)
    # [Kasia2] - now we have class MTrail in DSATUR.py
    trail_matrix = MTrail(num_of_nodes)
    M_trail = trail_matrix.M
    best_solution = BestSolution()
    x, y = np.ogrid[0:num_of_nodes, 0:num_of_nodes]
    # Algorithm
    for cycle in range(0, max_cycles):
        delta_M = np.zeros((num_of_nodes, num_of_nodes))
        for ant in range(0, n_ants):
            solution = dsatur(graph, trail_matrix, alpha, beta)
            # "chromatic" number
            q = max(solution)
            if q < best_solution.q:
                best_solution.q = q
                best_solution.colours = solution.copy()
            solution_arr = np.array(solution)
            delta_M = np.where(solution_arr[x] == solution_arr[y], delta_M[x, y],
                               delta_M[x, y] + (1 / q))
        M_trail = np.add(np.multiply(M_trail, p_coeff), delta_M)
    return best_solution


# TODO: why do we need M_trail?


if __name__ == "__main__":

    print("Chromatic number:")

    print(files[0])
    graph = file_to_graph(files[0])
    best_solution = ant_colony(graph)
    print(best_solution.q)
    print(best_solution.colours)

    # [Khanh] check if existing adjacent nodes have the same colour
    for e in graph.edges:
        # print(e[0])
        if (best_solution.colours[e[0] - 1] == best_solution.colours[e[1] - 1]):
            print("Bad situation occured! - wrong colouring")
            break

    # visualize coloured graph
    # visualizing_coloured_graph(graph, best_solution.colours)

    # visualize by netwulf
    visualizing_coloured_graph_by_netwulf(graph,best_solution.colours)