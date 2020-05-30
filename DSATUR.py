from read_graph import Graph


# I assumed that all of the graphs are undirected but we must check it!
# deg(...) functions works only if graphs are undirected.
# deg(...) - counts vertices degrees
def deg(graph: Graph):
    deg_l = [0] * len(graph.nodes)
    for edge in graph.edges:
        vertex_num = edge[0]
        deg_l[vertex_num - 1] += 1
    return deg_l


# choose_vert(...) - choose vertex with maximum saturation degree (and normal degree)
def choose_vert(neigh_colour_uncoloured, deg_l, uncoloured_node_list):
    # neigh_colour_uncoloured = list of lists with neighbour colours of uncoloured nodes
    # saturation degree = number of colours used in the neighbourhood of a vertex
    satur_deg = [len(colours) for colours in neigh_colour_uncoloured]
    max_satur = max(satur_deg)
    indices = [i for i, x in enumerate(satur_deg) if x == max_satur]
    if len(indices) == 1:
        # vertex = vertex with maximum saturation degree
        vertex = uncoloured_node_list[indices[0]]
    else:
        # choose vertex with maximum degree from among vertices with maximum saturation degree
        deg_uncoloured = [degree for j, degree in enumerate(deg_l) if j+1 in uncoloured_node_list]
        deg_uncoloured_max_satur = [degree for i, degree in enumerate(deg_uncoloured) if i in indices]
        max_deg = max(deg_uncoloured_max_satur)
        # vertex = first vertex with maximum degree
        i = deg_uncoloured_max_satur.index(max_deg)
        index = indices.index(i)
        vertex = uncoloured_node_list[index]
    return vertex


def colour_vert(vertex: int, neighbour_colours_l):
    new_colour = 1
    while new_colour in neighbour_colours_l[vertex - 1]:
        new_colour += 1
    return new_colour


def neigh_colours_update(vertex: int, vert_colour: int, edges, neighbour_colours_l, neighbour_colours_uncol, deg_l,
                         uncoloured_nodes_list):
    if deg_l[vertex - 1] == 0:
        return

    neighbour_vertex = [edges[index][1] for index, edge in enumerate(edges) if edges[index][0] == vertex]
    for neighbour in neighbour_vertex:
        if vert_colour not in neighbour_colours_l[neighbour - 1]:
            ind = neighbour - 1
            neighbour_colours_l[ind].append(vert_colour)
    neighbour_colours_uncol[:] = [colours for index, colours in enumerate(neighbour_colours_l) if
                               index + 1 in uncoloured_nodes_list]
    #neighbour_colours_uncol[:] = temporary_list.copy()
    return


def remove_from_uncoloured(current_vertex: int, uncoloured_nodes_list, neighbour_colours_uncol):
    index = uncoloured_nodes_list.index(current_vertex)
    neighbour_colours_uncol.pop(index)
    uncoloured_nodes_list.remove(current_vertex)
    if len(uncoloured_nodes_list) != len(neighbour_colours_uncol):
        raise Exception('num_of_uncoloured')


def dsatur(graph: Graph):
    num_of_nodes = len(graph.nodes)
    uncoloured_nodes = graph.nodes.copy()
    # neighbour_colours = list of colours used in the neighbourhood of a vertex
    neighbour_colours = [[] for i in range(num_of_nodes)]
    neighbour_colours_uncoloured = [[] for i in range(num_of_nodes)]
    vertex_colours = [0 for i in range(num_of_nodes)]
    deg_list = deg(graph)
    while uncoloured_nodes:
        current_vertex = choose_vert(neighbour_colours_uncoloured, deg_list, uncoloured_nodes)
        vertex_colours[current_vertex - 1] = colour_vert(current_vertex, neighbour_colours)
        neigh_colours_update(current_vertex, vertex_colours[current_vertex - 1], graph.edges, neighbour_colours,
                             neighbour_colours_uncoloured, deg_list, uncoloured_nodes)
        remove_from_uncoloured(current_vertex, uncoloured_nodes, neighbour_colours_uncoloured)
    return vertex_colours


# test
if __name__ == "__main__":
    edges1 = ((1, 2), (1, 3), (2, 1), (3, 1), (3, 4), (4, 3))
    graph1 = Graph(4, edges1)
    edges2 = ((1,2),(1,3),(2,1),(2,3),(3,1),(3,2))
    graph2 = Graph(4, edges2)
    edges3 = ((1, 3), (2, 3), (3, 1), (3, 2), (3, 4), (4, 3))
    graph3 = Graph(4, edges3)

    colours1 = dsatur(graph1)
    colours2 = dsatur(graph2)
    colours3 = dsatur(graph3)
    print(colours1)
    print(colours2)
    print(colours3)

