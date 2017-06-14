import os
import datetime
from src.evoAlgo import EvoAlgo
from src.loadData import LoadData
from src.representation import Representation

topology_catalog_path = "../tests/topology/"
config_catalog_path = "../tests/config/"
tc_catalog_path = "../tests/testcases/"
testCase_name = "TC_01"

folder_out = "../tests/result_representation/" + testCase_name + "_" + str(
    datetime.datetime.today().strftime("%Y.%m.%d-%H.%M.%S"))
tests = LoadData().read_testCase(tc_catalog_path + testCase_name)
if not os.path.exists(folder_out):
    os.makedirs(folder_out)
for test in tests:
    config_parameters = LoadData().read_config(config_catalog_path + test[1])
    rails_cost, ps_cost, population_quantity, selection_quantity, iterations_count, attempts_count = config_parameters
    cities_pos = LoadData().read_localization(topology_catalog_path + test[2])
    ps_pos = LoadData().read_localization(topology_catalog_path + test[3])

    for i in range(int(attempts_count)):
        evo_algo = EvoAlgo(cities_pos, ps_pos, int(rails_cost), int(ps_cost), int(population_quantity),
                           int(selection_quantity), int(iterations_count))
        evo_algo.generate_init_population()
        bests = evo_algo.start_evo_algo()
        result_representation = Representation()
        result_representation.save_chart(folder_out, testCase_name, test[0] + "_" + str(i + 1), bests, iterations_count)
        result_representation.save_graph(evo_algo.population[0].graph,
                                         folder_out, testCase_name, test[0] + "_" + str(i + 1),
                                         config_parameters,
                                         evo_algo.population[0].score, evo_algo.population[0].cities_score,
                                         evo_algo.population[0].ps_score, False)
        for individual in evo_algo.population:
            individual.print_tree()
            individual.count_score()
            print("Final Score: ", individual.score, " ", individual.cities_score, " ", individual.ps_score)
        print("The Best Score: ", evo_algo.population[0].score, " ", evo_algo.population[0].cities_score, " ",
              evo_algo.population[0].ps_score)
