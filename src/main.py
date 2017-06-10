from src.structs import RailNetworkTree
from src.loadData import LoadData

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

cities_pos = LoadData().read_localization(topology_catalog_path + cities_file_name)
ps_pos = LoadData().read_localization(topology_catalog_path + ps_file_name)

pos_dict = {}
for vertex, pos in cities_pos.items():
    pos_dict[vertex] = pos

for vertex, pos in ps_pos.items():
    pos_dict[vertex] = pos

RailNetworkTree(pos_dict)


