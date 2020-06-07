# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# [Test execution time] - different types of graph with the same number of nodes

from random import randrange
from ant_colony_alg import ant_colony
from graph_generator import bipartite_graph_generator, \
                            random_graph_generator, \
                            complete_graph_generator
from timeit import default_timer as timer
from statistics import mean, median

# number of nodes, number of ants and number of cycles for testing
nodes_list = [5, 10, 20]
n_ants_list = [5, 10, 20]
max_cycles_list = [5, 10, 20]


def test_time(graph, param_list, param_name: str):
    print("testing: " + param_name)
    solution_list = []
    times_stats = []
    for par in param_list:
        times = []
        temp = []
        # Find out which parameter for testing is on the list
        # 10 repetitions
        for i in range(10):
            if param_name == 'n_ants':
                start = timer()
                result = ant_colony(graph, par, 5)
                end = timer()
            elif param_name == 'max_cycles':
                start = timer()
                result = ant_colony(graph, 5, par)
                end = timer()
            else:
                raise Exception("bad parameter name")
            temp.append(result)
            times.append(end - start)
        temp_val_list = [t.q for t in temp]
        mean_val_res = mean(temp_val_list)
        mean_val = int(mean(times) * pow(10, 9))
        median_val = int(median(times) * pow(10, 9))
        max_val = int(max (times) * pow(10, 9))
        min_val = int(min(times) * pow(10, 9))
        solution_list.append(mean_val_res)
        times_stats.append((mean_val, median_val, min_val, max_val))
    return solution_list, times_stats


if __name__ == '__main__':
    with open('report_execution_time.txt', 'w') as file:
        file.writelines('Test execution time [picoseconds] for different graph types and nodes.\n\n')
        file.writelines('Nodes\t|N_ants\t|Cycles\t|\t\tBipartite\t\t|\t\tComplete\t\t|\t\tRandom\t\t\t|\n')
        file.writelines('\t\t\t|X_mean\tt_mean\tt_med\tt_min\tt_max\t|X_mean\tt_mean\tt_med\tt_min\tt_max\t|X_mean\tt_mean\tt_med\tt_min\tt_max\t\n')
        for non in nodes_list:
            # generate bipartite graph
            side1 = randrange(1, non-1)
            side2 = non-side1
            print('bipartite sides:')
            print(side1)
            print(side2)
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

            bip_sol_nants, bip_t_nants = test_time(bip_graph, n_ants_list, 'n_ants')
            bip_sol_cycles, bip_t_cycles = test_time(bip_graph, max_cycles_list, 'max_cycles')
            com_sol_nants, com_t_nants = test_time(com_graph, n_ants_list, 'n_ants')
            com_sol_cycles, com_t_cycles = test_time(com_graph, max_cycles_list, 'max_cycles')
            ran_sol_nants, ran_t_nants = test_time(ran_graph, n_ants_list, 'n_ants')
            ran_sol_cycles, ran_t_cycles = test_time(ran_graph, max_cycles_list, 'max_cycles')

            ind = 0
            for n_ants in n_ants_list:
                string_bip = '|'+ str(bip_sol_nants[ind]) + '\t' + str(bip_t_nants[ind][0]) + '\t' \
                             + str(bip_t_nants[ind][1]) + '\t' + str(bip_t_nants[ind][2]) + '\t' \
                             + str(bip_t_nants[ind][3]) + '\t'
                string_com = '|' + str(com_sol_nants[ind]) + '\t' + str(com_t_nants[ind][0]) + '\t' \
                             + str(com_t_nants[ind][1]) + '\t' + str(com_t_nants[ind][2]) + '\t' \
                             + str(com_t_nants[ind][3]) + '\t'
                string_ran = '|' + str(ran_sol_nants[ind]) + '\t' + str(ran_t_nants[ind][0]) + '\t' \
                             + str(ran_t_nants[ind][1]) + '\t' + str(ran_t_nants[ind][2]) + '\t' \
                             + str(ran_t_nants[ind][3]) + '\t'

                file.writelines(str(non) + '\t' + str(n_ants) + '\t5\t' + string_bip + string_com + string_ran + '\n')
                ind += 1

            ind = 0
            for cycle in max_cycles_list:
                string_bip = '|'+ str(bip_sol_cycles[ind]) + '\t' + str(bip_t_cycles[ind][0]) + '\t' \
                             + str(bip_t_cycles[ind][1]) + '\t' + str(bip_t_cycles[ind][2]) + '\t' \
                             + str(bip_t_cycles[ind][3]) + '\t'
                string_com = '|' + str(com_sol_cycles[ind]) + '\t' + str(com_t_cycles[ind][0]) + '\t' \
                             + str(com_t_cycles[ind][1]) + '\t' + str(com_t_cycles[ind][2]) + '\t' \
                             + str(com_t_cycles[ind][3]) + '\t'
                string_ran = '|' + str(ran_sol_cycles[ind]) + '\t' + str(ran_t_cycles[ind][0]) + '\t' \
                             + str(ran_t_cycles[ind][1]) + '\t' + str(ran_t_cycles[ind][2]) + '\t' \
                             + str(ran_t_cycles[ind][3]) + '\t'

                file.writelines(str(non) + '\t5\t' + str(cycle)+ '\t' + string_bip + string_com + string_ran + '\n')
                ind += 1

        file.close()

    print("Finish execution time test!")