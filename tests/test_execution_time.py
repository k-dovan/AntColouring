# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# [Test execution time] - different types of graph with the same number of nodes

from random import randrange
from ant_colony_alg import ant_colony
from read_graph import file_to_graph
from graph_generator import bipartite_graph_generator, \
                            random_graph_generator, \
                            complete_graph_generator, \
                            one_vert_connected_graph_generator
from visualizing_graph import visualize_original_graph_by_netwulf
import time

# number of node for testing
number_of_nodes = [20, 50, 100, 150]

if __name__ == '__main__':
    with open('report_execution_time.txt', 'w') as file:
        file.writelines('Test execution time for different graph types and nodes.\n\n')
        file.writelines('Nodes\t\t|\t\tBipartite\t\t|\t\tComplete\t\t|\t\tRandom\t\t\t|\n')
        file.writelines('\t\t\t|\tTime\tChromatic\t|\tTime\tChromatic\t|\tTime\tChromatic\t|\n')
        for non in number_of_nodes:
            # generate bipartite graph
            side1 = randrange(1, non-1)
            side2 = non-side1
            min_edges = 1
            max_edges = side1*side2
            number_of_edges = randrange(min_edges, max_edges)
            bip_graph = bipartite_graph_generator(side1, side2,number_of_edges)

            # generate complete graph
            com_graph = complete_graph_generator(non)

            # generate random graph
            ran_min_edges = int(non*(non-1)/10)
            ran_max_edges = int(non*(non-1)/2)
            ran_graph_edges = randrange(ran_min_edges, ran_max_edges)
            ran_graph = random_graph_generator(non, ran_graph_edges)

            start_bip = time.time()
            bip_sol = ant_colony(bip_graph, n_ants=20, max_cycles=5, p_coeff=0.5, alpha=2, beta=4)
            elapsed_time_bip = time.time() - start_bip

            start_com = time.time()
            com_sol = ant_colony(com_graph, n_ants=20, max_cycles=5, p_coeff=0.5, alpha=2, beta=4)
            elapsed_time_com = time.time() - start_com

            start_ran = time.time()
            ran_sol = ant_colony(ran_graph, n_ants=20, max_cycles=5, p_coeff=0.5, alpha=2, beta=4)
            elapsed_time_ran = time.time() - start_ran

            file.writelines('\n\n' + str(non) + '\t\t\t' +
                            '{:10.4f}'.format(elapsed_time_bip) + '\t\t' + str(bip_sol.q) +'\t\t' +
                            '{:10.4f}'.format(elapsed_time_com) + '\t\t' + str(com_sol.q) +'\t\t' +
                            '{:10.4f}'.format(elapsed_time_ran) + '\t\t' + str(ran_sol.q))

        file.close()

    print("Finish execution time test!")