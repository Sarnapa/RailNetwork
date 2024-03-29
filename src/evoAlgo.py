from src.structs import RailNetworkTree
from random import random
from bisect import bisect_left


class EvoAlgo:

    def __init__(self, cities_pos, ps_pos, rails_cost, ps_cost, population_quantity, selection_quantity, iterations_count):
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
        self.selection_quantity = selection_quantity
        self.iterations_count = iterations_count
        self.population = []

    def start_evo_algo(self):
        best_results = []

        for i in range(self.iterations_count):
            print("Iteration: ", i + 1)
            result = self.start_one_iter()
            best_results.append(result)

        return best_results

    def start_one_iter(self):
        selected_individuals = self.do_selection()
        children_list = self.do_crossover(selected_individuals)
        mutated_list = self.do_mutation(children_list)
        self.do_succession(mutated_list)
        best_cost = self.population[0].score

        return best_cost

    def generate_init_population(self):
        for i in range(self.population_quantity):
            individual = RailNetworkTree(self.pos_dict, self.rails_cost, self.ps_cost)
            individual.generate_init_tree()
            self.population.append(individual)

    def do_selection(self):
        selected_individuals = []
        scores_list = []
        last_score = 0
        population = self.population.copy()
        for individual in self.population:
            last_score += 1/individual.count_score()
            scores_list.append(last_score)
        for i in range(self.selection_quantity):
            rand = random() * scores_list[-1]
            if rand in scores_list:
                rand_pos = scores_list.index(rand)
            else:
                rand_pos = bisect_left(scores_list, rand)
            selected_individuals.append(population[rand_pos])
            tmp_pos = rand_pos + 1
            for j in range(tmp_pos, len(population)):
                scores_list[j] -= 1/population[rand_pos].score
            scores_list.remove(scores_list[rand_pos])
            population.remove(population[rand_pos])

        return selected_individuals

    def do_crossover(self, selected_individuals):
        children_list = []
        length = len(selected_individuals)

        for i in range(length - 1):
            for j in range(i + 1, length):
                child = RailNetworkTree(self.pos_dict, self.rails_cost, self.ps_cost)
                child.crossover(selected_individuals[i].get_cities_edges(), selected_individuals[j].get_cities_edges())
                child.connect_ps(selected_individuals[i].get_ps_edges(), selected_individuals[j].get_ps_edges())
                children_list.append(child)

        return children_list

    def do_mutation(self, children_list):

        for child in children_list:
            child.mutate()

        return children_list

    def do_succession(self, mutated_list):
        population = self.population.copy()
        for mutated in mutated_list:
            population.append(mutated)
        for individual in population:
            individual.count_score()
        sorted_population = sorted(population, key=lambda individual: individual.score)
        self.population = sorted_population[:self.population_quantity]
        print("After succession:")
        for individual in self.population:
            #individual.print_tree()
            print("Individual score: ", individual.score, " ", individual.cities_score, " ", individual.ps_score)