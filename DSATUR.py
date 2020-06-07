# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# DSATUR algorithm implementation
from read_graph import Graph, file_to_graph, files
from random import choice, random
from math import pow
import numpy as np

# [Kasia2]
# Trail matrix
class MTrail:
    def __init__(self, num_of_nodes):
        self.M = np.ones((num_of_nodes, num_of_nodes))


# deg(...) - counts vertices degrees
def deg(graph: Graph):
    deg_l = [0] * len(graph.nodes)
    for edge in graph.edges:
        vertex_num = edge[0]
        deg_l[vertex_num - 1] += 1
    return deg_l


# choose_vert...(...) - choose vertex with maximum saturation degree (and normal degree)
def choose_vert(neigh_colour_uncoloured, deg_l, uncoloured_node_list):
    # neigh_colour_uncoloured = list of lists with neighbour colours of uncoloured nodes
    # saturation degree = number of colours used in the neighbourhood of a vertex
    satur_deg = [len(colours) for colours in neigh_colour_uncoloured]
    max_satur = max(satur_deg)
    indices_max_satur = [i for i, x in enumerate(satur_deg) if x == max_satur]
    if len(indices_max_satur) == 1:
        # vertex = vertex with maximum saturation degree
        vertex = uncoloured_node_list[indices_max_satur[0]]
    else:
        # choose vertex with maximum degree from among vertices with maximum saturation degree
        deg_uncoloured = [degree for j, degree in enumerate(deg_l) if j + 1 in uncoloured_node_list]
        deg_uncoloured_max_satur = [degree for i, degree in enumerate(deg_uncoloured) if i in indices_max_satur]
        max_deg = max(deg_uncoloured_max_satur)
        # vertex = random vertex with maximum degree (if we have more than one)
        indices_max_deg = [i for i, x in enumerate(deg_uncoloured_max_satur) if x == max_deg]
        i = choice(indices_max_deg)
        vertex = uncoloured_node_list[i]
    return vertex


# colour_vert(...) - return smallest possible colour
def colour_vert(vertex: int, neighbour_colours_l):
    new_colour = 1
    while new_colour in neighbour_colours_l[vertex - 1]:
        new_colour += 1
    return new_colour


# neigh_colours_update(...) - updates 2 lists of neighbour colours: for each node and for uncoloured nodes,
# after assigning colour to one node
def neigh_colours_update(vertex: int, vert_colour: int, edges, neighbour_colours_l, neighbour_colours_uncol, deg_l,
                         uncoloured_nodes_list):
    if deg_l[vertex - 1] == 0:
        return

    # neighbour_vertex = [edges[index][1] for index, edge in enumerate(edges) if edges[index][0] == vertex]
    # [Khanh] examine both cases: neighbour number is less than OR greater than vertex
    neighbour_vertex = [edges[index][0] for index, edge in enumerate(edges) if edges[index][1] == vertex] + \
                       [edges[index][1] for index, edge in enumerate(edges) if edges[index][0] == vertex]
    # [Khanh] remove duplicate neighbours if graph is not simple graph (In fact, it should be)
    # [Kasia] it must be simple. Otherwise we can't colour it
    neighbour_vertex = list(set(neighbour_vertex))

    for neighbour in neighbour_vertex:
        if vert_colour not in neighbour_colours_l[neighbour - 1]:
            ind = neighbour - 1
            neighbour_colours_l[ind].append(vert_colour)

    # [Kasia] vertex should also remember his own colour
    neighbour_colours_l[vertex - 1].append(vert_colour)
    neighbour_colours_uncol[:] = [colours for index, colours in enumerate(neighbour_colours_l) if
                                  index + 1 in uncoloured_nodes_list]
    return


# [Kasia2]
# colour_groups_update(...)- add coloured vertex to the special colour group
def colour_groups_update(vertex: int, colour: int, colour_groups_l):
    if len(colour_groups_l) < colour:
        colour_groups_l.append([vertex])
    else:
        colour_groups_l[colour - 1].append(vertex)


# [Kasia]
# uncoloured_check(...) - integrity check
def uncoloured_check(neighbour_colours_l, neighbour_colours_uncol, uncoloured_nodes_list):
    if len(neighbour_colours_uncol) != len(uncoloured_nodes_list):
        raise Exception("neighbour_colours_uncoloured) != len(uncoloured_nodes)")
    for i in range(len(uncoloured_nodes_list)):
        i2 = uncoloured_nodes_list[i] - 1
        if neighbour_colours_l[i2] != neighbour_colours_uncol[i]:
            raise Exception("neighbour_colours and neighbour_colours_uncoloured not coherent")


def remove_from_uncoloured(current_vertex: int, uncoloured_nodes_list, neighbour_colours_uncol):
    index = uncoloured_nodes_list.index(current_vertex)
    neighbour_colours_uncol.pop(index)
    uncoloured_nodes_list.remove(current_vertex)
    if len(uncoloured_nodes_list) != len(neighbour_colours_uncol):
        raise Exception('num_of_uncoloured')


# [Kasia2]
# trail factor tau2 - page 298 in A. Hertz "Ants can colour graphs"
def trail_factor(vertex: int, colour: int, graph, colour_groups_l, M_trail):
    num_of_nodes = len(graph.nodes)
    if len(colour_groups_l) < colour:
        return 1
    this_colour_group = colour_groups_l[colour - 1]
    if this_colour_group:
        x, y = np.ogrid[0:num_of_nodes, 0:num_of_nodes]
        vert_trails = np.where(x == vertex - 1, M_trail[x, y], 0)
        sum_of_trails = np.sum(vert_trails)
        trail_f = sum_of_trails / len(this_colour_group)
    else:
        trail_f = 1
    return trail_f


# [Kasia2] - first strategy shown in ANT_DSATUR procedure on page 300
#           in A. Hertz "Ants can colour graphs"
# probability_uncol_choice(...) - probability of choosing exact uncoloured vertex
def probability_uncol_choice(vertex: int, colour: int, graph, colour_groups_l, M_trail, neighbour_colours,
                             alpha_1: float, beta_1: float, partial_solution):
    trail_list = [trail_factor(index + 1, current_colour, graph, colour_groups_l, M_trail) for index, current_colour in
                  enumerate(partial_solution) if current_colour > 0]
    trail_1 = trail_factor(vertex, colour, graph, colour_groups_l, M_trail)
    # first strategy - eta_1 coefficient equal to saturation degree
    satur_deg_list = [len(colours) for colours in neighbour_colours]
    satur_deg = [len(colours) for (colours, current_colour) in zip(neighbour_colours, partial_solution) if current_colour > 0]
    if len(satur_deg) != len(trail_list):
        raise Exception('len(satur_deg) != len(trail_list)')
    numerator = pow(float(trail_1), alpha_1) * pow(float(satur_deg_list[vertex - 1]), beta_1)
    trail_list_power = [pow(float(trail), alpha_1) for trail in trail_list]
    satur_power = [pow(float(satur), beta_1) for satur in satur_deg]
    denominator_list = [trl * sat for (trl, sat) in zip(trail_list_power, satur_power)]
    denominator = sum(denominator_list)
    p_it = numerator / denominator
    return p_it


# [Kasia2] - new way of vertex choice
# choose_vert_dsatur(...) - choose vertex according to first staregy shown in ANT_DSATUR procedure on page 300
# # #           in A. Hertz "Ants can colour graphs"
def choose_vert_dsatur(graph, colour_groups_l, M_trail, neighbour_colours,
                       alpha_1: float, beta_1: float, partial_solution, uncoloured_vertice, neigh_colour_uncoloured, deg_l):
    # first must be chosen traditionally - otherwise it doesn't work
    if not colour_groups_l:
        vertex = choose_vert(neigh_colour_uncoloured, deg_l, uncoloured_vertice)
        colour = colour_vert(vertex, neighbour_colours)
        return vertex, colour
    p_it_list = []
    for vertex in uncoloured_vertice:
        colour = colour_vert(vertex, neighbour_colours)
        p_it = probability_uncol_choice(vertex, colour, graph, colour_groups_l, M_trail, neighbour_colours, alpha_1,
                                        beta_1, partial_solution)
        p_it_list.append(p_it)

        rand_float = random()
        if rand_float <= p_it:
            return vertex, colour

    # [Kasia2] - if we get no vertex after choice repetition we randomly get the one with maximum probability
    max_p_it = max(p_it_list)
    # [Khanh2] - randomly pick among best candidates
    indexes = [i for i, p in enumerate(p_it_list) if p == max_p_it]
    random_index = choice(indexes)
    vertex = uncoloured_vertice[random_index]
    colour = colour_vert(vertex, neighbour_colours)
    return vertex, colour

# [Kasia2] - additional argument: trail_matrix: MTrail
# dsatur(...) - DSATUR algorithm implementation
def dsatur(graph: Graph, trail_matrix: MTrail, alpha, beta):
    # [Kasia2] - additional argument: trail_matrix: MTrail
    M_trail = trail_matrix.M
    num_of_nodes = len(graph.nodes)
    uncoloured_nodes = graph.nodes.copy()
    # neighbour_colours = list of colours used in the neighbourhood of a vertex
    neighbour_colours = [[] for i in range(num_of_nodes)]
    neighbour_colours_uncoloured = [[] for i in range(num_of_nodes)]
    vertex_colours = [0 for i in range(num_of_nodes)]
    # [Kasia2] We need vertice grouped by a colour
    colour_groups = []
    deg_list = deg(graph)
    iteration = 0
    while uncoloured_nodes:
        # [Kasia] integrity check
        iteration += 1
        # print('iteration'+str(iteration))
        uncoloured_check(neighbour_colours, neighbour_colours_uncoloured, uncoloured_nodes)
        current_vertex, colour = choose_vert_dsatur(graph, colour_groups, M_trail, neighbour_colours, alpha, beta,
                                                    vertex_colours, uncoloured_nodes, neighbour_colours_uncoloured, deg_list)
        vertex_colours[current_vertex - 1] = colour
        neigh_colours_update(current_vertex, vertex_colours[current_vertex - 1], graph.edges, neighbour_colours,
                             neighbour_colours_uncoloured, deg_list, uncoloured_nodes)
        colour_groups_update(current_vertex, vertex_colours[current_vertex - 1], colour_groups)
        remove_from_uncoloured(current_vertex, uncoloured_nodes, neighbour_colours_uncoloured)
    return vertex_colours


# test
if __name__ == "__main__":
    edges1 = ((1, 2), (1, 3), (2, 1), (3, 1), (3, 4), (4, 3))
    graph1 = Graph(4, edges1)
    graph2 = file_to_graph(files[2])

    trail_matrix = MTrail(len(graph1.nodes))
    trail_matrix2 = MTrail(len(graph2.nodes))

    colours1 = dsatur(graph1, trail_matrix)
    print(colours1)
    colours2 = dsatur(graph2, trail_matrix2)
    print(colours2)
