# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# Test - parameters
from ant_colony_alg import ant_colony
from read_graph import file_to_graph
from statistics import mean, median

in_files = ['myciel3.col', 'queen5_5.col', 'jean.col']

# Parameters to test
n_ants_list = [5, 20, 40]
max_cycles_list = [5, 20, 40]
p_coeff_list = [0.4, 0.5, 0.6]
alpha_list = [0, 2, 4]
beta_list = [0, 2, 4]


def test_func(graph, param_list, param_name: str):
    print("testing: " + param_name)
    solution_list = []
    for par in param_list:
        temp = []
        # Find out which parameter for testing is on the list
        for i in range(10):
            if param_name == 'n_ants':
                result = ant_colony(graph, par, 5)
            elif param_name == 'max_cycles':
                result = ant_colony(graph, 20, par)
            elif param_name == 'p_coeff':
                result = ant_colony(graph, 20, 5, par)
            elif param_name == 'alpha':
                result = ant_colony(graph, 20, 5, alpha=par)
            elif param_name == 'beta':
                result = ant_colony(graph, 20, 5, beta=par)
            else:
                raise Exception("bad parameter name")
            temp.append(result)
        temp_val_list = [t.q for t in temp]
        mean_val = mean(temp_val_list)
        median_val = median(temp_val_list)
        max_val = max (temp_val_list)
        min_val = min(temp_val_list)
        solution_list.append((mean_val, median_val, max_val, min_val))
    return solution_list


if __name__ == '__main__':
    with open('report_params.txt', 'w') as file:
        for file_graph in in_files:
            # n_ants test
            graph = file_to_graph(file_graph)
            file.write(
                'File: ' + file_graph + '; nodes: ' + str(len(graph.nodes)) + '; edges: ' + str(len(graph.edges)) + '\n\n')

            # Testing
            solutions = []
            solutions.append(test_func(graph, n_ants_list, 'n_ants'))
            solutions.append(test_func(graph, max_cycles_list, 'max_cycles'))
            solutions.append(test_func(graph, p_coeff_list, 'p_coeff'))
            solutions.append(test_func(graph, alpha_list, 'alpha'))
            solutions.append(test_func(graph, beta_list, 'beta'))

            # Create report
            headers = ['n_ants', 'max_cycles', 'p_coeff', 'alpha', 'beta']
            params_lists = [n_ants_list, max_cycles_list, p_coeff_list, alpha_list, beta_list]
            for i in range(len(headers)):
                header = headers[i]
                test_solution = solutions[i]
                test_param = params_lists[i]

                file.write(header + ' test:\n')
                file.write(header + '\tmean\tmedian\tmax\tmin\n')
                for i in range(len(test_solution)):
                    solution = test_solution[i]
                    param = test_param[i]
                    file.write(str(param) + '\t' + str(solution[0]) + '\t' + str(solution[1]) + '\t' + str(solution[2]) + '\t' + str(solution[3]) + '\n')
                file.write('\n\n')

            file.write('\n\n\n')

        file.close()

