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


def ant_colony(graph: Graph, n_ants=3, max_cycles=3, p_coeff=0.9):
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
    # edges1 = ((1, 2), (1, 3), (2, 1), (3, 1), (3, 4), (4, 3))
    # graph1 = Graph(4, edges1)

    graph2 = file_to_graph(files[2])
    best_solution = ant_colony(graph2)
    print("best_solution and best_q")
    print(best_solution.q)
    print(best_solution.colours)
    print(len(best_solution.colours))

    # [Khanh] check if existing adjacent nodes have the same colour
    for e in graph2.edges:
        # print(e[0])
        if(best_solution.colours[e[0]-1] == best_solution.colours[e[1]-1]):
            print ("Bad situation occured!")
            break
