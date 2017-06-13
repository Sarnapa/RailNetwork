from src.evoAlgo import EvoAlgo
from src.structs import RailNetworkTree
from src.loadData import LoadData
from src.representation import Representation

topology_catalog_path = "../tests/topology/"
config_catalog_path = "../tests/config/"
cities_file_name = "Test03_cities"
ps_file_name = "Test03_power_stations"
config_file_name = "Config_01"

rails_cost, ps_cost, population_quantity, selection_quantity, iterations_count, attempts_count = LoadData().read_config(config_catalog_path + config_file_name)
cities_pos = LoadData().read_localization(topology_catalog_path + cities_file_name)
ps_pos = LoadData().read_localization(topology_catalog_path + ps_file_name)
print(rails_cost, ps_cost, population_quantity, selection_quantity, iterations_count, attempts_count)

evo_algo = EvoAlgo(cities_pos, ps_pos, int(rails_cost), int(ps_cost), int(population_quantity), int(selection_quantity), int(iterations_count), int(attempts_count))
evo_algo.generate_init_population()
evo_algo.start_evo_algo(None, None)
result_representation = Representation()
for individual in evo_algo.population:
    individual.print_tree()
    individual.count_score()
    print("FINAL SCORE: ", individual.score)
print("THE BEST SCORE: ", evo_algo.population[0].score)
result_representation.show_graph(evo_algo.population[0].graph)
