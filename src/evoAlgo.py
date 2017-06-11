from src.structs import RailNetworkTree

class EvoAlgo:

    def __init__(self, cities_pos, ps_pos, rails_cost, ps_cost, population_quantity, iterations_count, attempts_count):
        self.cities_pos = cities_pos
        self.ps_pos = ps_pos
        self.pos_dict = {}
        for vertex, pos in cities_pos.items():
            self.pos_dict[vertex] = pos

        for vertex, pos in ps_pos.items():
            self.pos_dict[vertex] = pos
        self.rails_cost = rails_cost
        self.ps_cost = ps_cost
        self.population_quantity = population_quantity
        self.iterations_count = iterations_count
        self.attempts_count = attempts_count
        self.population = []

    def start_evo_algo(self, input_filename, path_to_report):
        best_results = []

        for i in range(self.iterations_count):
            result = self.start_one_iter()
            # jakies kwestie zwiazane z generowanie raportów

        return best_results

    def start_one_iter(self):
        best_cost = 0.0
        avg_cost = 0.0

        #algorytm

        return [best_cost, avg_cost] # pewnie więcej bedzie tutaj parametrow na outpucie

    def generate_init_population(self):

        for i in range(self.population_quantity):
            individual = RailNetworkTree(self.pos_dict)
            individual.generate_init_tree()
            individual.print_tree()
            self.population.append(individual)



    def do_selection(self):
        return