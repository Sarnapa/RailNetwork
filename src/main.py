from src.evoAlgo import EvoAlgo
from src.loadData import LoadData
from src.structs import RailNetworkTree

'''points = set()
points.add((1,2))
points.add((6,7))
points.add((3,4))
points.add((8,9))

something = points.pop() + (0,0,)
print(something)'''

topology_catalog_path = "../tests/topology/"
cities_file_name = "Test01_cities"
ps_file_name = "Test01_power_stations"

rails_cost, ps_cost, opulation_quantity, selection_quantity, iterations_count, attempts_count = LoadData().read_config("../tests/config/Config_01")
cities_pos = LoadData().read_localization(topology_catalog_path + cities_file_name)
ps_pos = LoadData().read_localization(topology_catalog_path + ps_file_name)
print (rails_cost, ps_cost, opulation_quantity, selection_quantity, iterations_count, attempts_count)
#na razie tak
#evo_algo = EvoAlgo(cities_pos, ps_pos, 10, 5, 2, 2, 0, 0)
evo_algo = EvoAlgo(cities_pos, ps_pos,rails_cost, ps_cost, opulation_quantity, selection_quantity, iterations_count, attempts_count)
evo_algo.generate_init_population()
selected = evo_algo.do_selection()
evo_algo.do_crossover(selected)

