from src.utils import distanceBetweenPoints
from random import sample, random
import networkx as nx
import sys
import operator


class RailNetworkTree:
    def __init__(self, pos_dict: dict, rails_cost, ps_cost):
        self.score = sys.float_info.max
        self.rails_cost = rails_cost
        self.ps_cost = ps_cost
        self.cities_nodes = set()
        self.ps_nodes = set()
        self.connected_ps_nodes = set()
        self.graph = nx.Graph()
        for vertex, pos in pos_dict.items():
            self.graph.add_node(vertex, x=pos[0], y=pos[1])
            if vertex < 0:
                self.ps_nodes.add(vertex)
            else:
                self.cities_nodes.add(vertex)

    def get_node_x(self, vertex):
        return self.graph.node[vertex]['x']

    def get_node_y(self, vertex):
        return self.graph.node[vertex]['y']

    def get_node_pos(self, vertex):
        return self.get_node_x(vertex), self.get_node_y(vertex)

    def get_cities_edges(self):
        cities_edges = []
        for v1, v2 in self.graph.edges():
            if v1 >= 0 and v2 >= 0:
                cities_edges.append((v1, v2, self.graph[v1][v2]))
        return cities_edges

    def get_ps_edges(self):
        ps_edges = []
        for v1, v2 in self.graph.edges():
            if v1 < 0 or v2 < 0:
                ps_edges.append((v1, v2, self.graph[v1][v2]))
        return ps_edges

    def add_edge(self, v1, v2):
        self.graph.add_edge(v1, v2, weight=distanceBetweenPoints(self.get_node_pos(v1) + (0,), self.get_node_pos(v2) + (0,)))
        if v1 < 0 and v1 not in self.connected_ps_nodes:
            self.connected_ps_nodes.add(v1)
        elif v2 < 0 and v2 not in self.connected_ps_nodes:
            self.connected_ps_nodes.add(v2)

    def remove_edge(self, v1, v2):
        self.graph.remove_edge(v1, v2)
        if v1 < 0 and v1 in self.connected_ps_nodes:
            self.connected_ps_nodes.remove(v1)
        elif v2 < 0 and v2 in self.connected_ps_nodes:
            self.connected_ps_nodes.remove(v2)

    # na razie tak - trzeba pomyslec z ta funkcja
    def count_score(self):
        cities_to_find_ps_conn = self.cities_nodes.copy()
        #ps_score = 0
        #cities_score = 0
        self.score = 0
        for v1, v2 in self.graph.edges():
            if v1 < 0 or v2 < 0:
                if v1 >= 0:
                    cities_to_find_ps_conn.remove(v1)
                elif v2 >= 0:
                    cities_to_find_ps_conn.remove(v2)
                #print("KOSZT ODCINEK: ", self.ps_cost * self.graph[v1][v2]['weight'], " ", v1, " ", v2)
                self.score += self.ps_cost * self.graph[v1][v2]['weight']
                #ps_score += self.ps_cost * self.graph[v1][v2]['weight']
            else:
                #print("KOSZT ODCINEK: ", self.rails_cost * self.graph[v1][v2]['weight'], " ", v1, " ", v2)
                self.score += self.rails_cost * self.graph[v1][v2]['weight']
                #cities_score += self.rails_cost * self.graph[v1][v2]['weight']
        for city in cities_to_find_ps_conn:
            #print("KOSZT ODCINEK: ", self.ps_cost * self.distance_to_nearest_ps(city), " miasto: ", city)
            self.score += self.ps_cost * self.distance_to_nearest_ps(city)
            #ps_score += self.ps_cost * self.distance_to_nearest_ps(city)
        #print("SCORE: ", self.score, " ", ps_score, " ", cities_score)
        return self.score

    def distance_to_nearest_ps(self, node):
        distance = sys.float_info.max
        for ps_node in self.connected_ps_nodes:
            tmp_distance = nx.shortest_path_length(self.graph, node, ps_node, 'weight')
            if tmp_distance < distance:
                distance = tmp_distance
        #print("WYNIK: ", distance, " ", node)
        return distance

    def generate_init_tree(self):
        used_nodes = set()
        not_used_nodes = self.cities_nodes.copy()
        while len(not_used_nodes) != 0:
            node = sample(not_used_nodes, 1)
            node = node.pop(0)
            not_used_nodes.remove(node)
            if len(used_nodes) == 0:
                used_nodes.add(node)
            else:
                second_node = sample(used_nodes, 1)
                second_node = second_node.pop(0)
                self.add_edge(node, second_node)
                used_nodes.add(node)

        if len(used_nodes) != 0:
            not_used_nodes = self.ps_nodes.copy()
            while len(not_used_nodes) != 0:
                node = sample(not_used_nodes, 1)
                node = node.pop(0)
                not_used_nodes.remove(node)
                second_node = sample(used_nodes, 1)
                second_node = second_node.pop(0)
                # remove second_node because one city can be connected with one power station
                used_nodes.remove(second_node)
                self.add_edge(node, second_node)

    def mutate(self):
        added_edge = self.addCycleToGraph()
        print("added_edge: ", added_edge)
        if added_edge[0] < 0:
            neighbours = self.graph.neighbors(added_edge[0])
            neighbours.remove(added_edge[1])
            self.remove_edge(added_edge[0], neighbours[0])
        elif added_edge[1] < 0:
            neighbours = self.graph.neighbors(added_edge[1])
            neighbours.remove(added_edge[0])
            self.remove_edge(added_edge[1], neighbours[0])
        else:
            edges_to_remove = list(nx.find_cycle(self.graph))
            edges_to_remove.remove(added_edge)
            edge_to_remove = sample(edges_to_remove, 1)
            v1, v2 = edge_to_remove
            print("lolo: ", edge_to_remove, " ", v1, " ", v2)
            self.remove_edge(v1, v2)

    def addCycleToGraph(self):
        do = True
        while do:
            nodes = sample(self.graph.nodes(), 2)
            if not (self.graph.has_edge(nodes[0], nodes[1]) or self.graph.has_edge(nodes[1], nodes[0])):
                self.add_edge(nodes[0], nodes[1])
                return nodes[0], nodes[1]

    def crossover(self, edges1, edges2):
        g = nx.Graph()
        g.add_edges_from(edges1)
        g.add_edges_from(edges2)
        mst = nx.minimum_spanning_edges(g, 'weight')
        edge_list = list(mst)
        self.graph.add_edges_from(edge_list)

    def connect_ps(self, edges1, edges2):
        edges = {}
        for ps_node in self.ps_nodes:
            edges[ps_node] = set()
        for edge in edges1:
            if edge[0] < 0:
                edges[edge[0]].add((edge[1], edge[2]['weight']))
            elif edge[1] < 0:
                edges[edge[1]].add((edge[0], edge[2]['weight']))
        for edge in edges2:
            if edge[0] < 0:
                edges[edge[0]].add((edge[1], edge[2]['weight']))
            elif edge[1] < 0:
                edges[edge[1]].add((edge[0], edge[2]['weight']))
        for ps_node in self.ps_nodes:
            sorted_edges = sorted(edges[ps_node], key=operator.itemgetter(1))
            edges[ps_node] = sorted_edges

        ps_nodes = self.ps_nodes.copy()
        connected_cities = []
        for i in range(len(ps_nodes)):
            node = sample(ps_nodes, 1).pop(0)
            edge = sample(edges[node], 1)
            node2, weight = edge[0]
            current_score = self.score
            self.add_edge(node2, node)
            if node2 in connected_cities:
                self.remove_edge(node2, node)
            elif self.count_score() > current_score:
                self.remove_edge(node2, node)
            else:
                connected_cities.append(node2)
                ps_nodes.remove(node)

    # na razie dla testow
    def print_tree(self):
        print("Tree:")
        print("Nodes:")
        for node in self.graph.nodes():
            print(node, end=" ")
            print("(", self.get_node_x(node), ",", self.get_node_y(node), ")")
        print("Edges:")
        for v1, v2 in self.graph.edges():
            print(v1, "->", v2, "length: ", self.graph[v1][v2]['weight'])