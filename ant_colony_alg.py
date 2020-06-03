# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
from DSATUR import dsatur
from read_graph import Graph, file_to_graph, files
import numpy as np


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


def ant_colony(graph: Graph, n_ants=3, max_cycles=3, p_coeff=0.9):
    is_simple_undirected(graph)
    # Variables
    num_of_nodes = len(graph.nodes)
    M_trail = np.ones((num_of_nodes, num_of_nodes))
    best_solution = BestSolution()
    x, y = np.ogrid[0:num_of_nodes, 0:num_of_nodes]
    # Algorithm
    for cycle in range(1, max_cycles):
        delta_M = np.zeros((num_of_nodes, num_of_nodes))
        for ant in range(1, n_ants):
            solution = dsatur(graph)
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
    for graph in files:
        print(graph)
        graph2 = file_to_graph(graph)
        best_solution = ant_colony(graph2, 10, 10)
        print(best_solution.q)

        # [Khanh] check if existing adjacent nodes have the same colour
        for e in graph2.edges:
            # print(e[0])
            if(best_solution.colours[e[0]-1] == best_solution.colours[e[1]-1]):
                print ("Bad situation occured! - wrong colouring")
                break
