# Katarzyna Rzeczyca, Van Khanh Do
# Ant colouring algorithm
# Grafy i sieci
#
# Test - parameters
from ant_colony_alg import ant_colony
from read_graph import file_to_graph
from statistics import mean, median

in_files = ['myciel3.col', 'myciel4.col', 'queen5_5.col']
chromatic_numbers = [4, 5, 5]

if __name__ == '__main__':
    with open('report_chromatic.txt', 'w') as file:
        iteration = 0
        for file_graph in in_files:
            graph = file_to_graph(file_graph)
            file.write(
                'File: ' + file_graph + '; nodes: ' + str(len(graph.nodes)) + '; edges: ' + str(len(graph.edges)))
            file.write('; chromatic number: ' + str(chromatic_numbers[iteration]) + '\n\n')

            # todo range 10, ant col params
            # Run ant_colony using best parameters found in previous tests
            results = []
            for i in range(1):
                # todo parameters
                results.append(ant_colony(graph, 20, 5))

            file.write('colouring achieved:\n')
            results_chromatic = [res.q for res in results]
            file.write(str(results_chromatic))
            file.write('\n\n')

            iteration += 1
        file.close()

    print("Finish chromatic test!")