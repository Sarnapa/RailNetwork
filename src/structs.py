from src.utils import distanceBetweenPoints
from random import sample, random
import networkx as nx


class RailNetworkTree:
    def __init__(self, pos_dict: dict):
        self.cities_nodes = set()
        self.ps_nodes = set()
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

    def count_goal_fun(self, cost_traction, cost_add_electic_station):
        print("count goal func")

    def mutate(self):
        edges_to_remove = self.addCycleToGraph()
        edge_to_remove = random.sample(edges_to_remove,1)
        self.graph.remove_edge(edge_to_remove)

    def addCycleToGraph(self):
        do = True
        while (do):
            nodes = random.sample(self.graph.nodes(), 2)
            if not (self.graph.has_edge(nodes[0], nodes[1]) or self.graph.has_edge(nodes[1], nodes[0])):
                self.graph.add_edge(nodes[0], nodes[1])
                if (nx.is_directed_acyclic_graph(self.graph)):
                    self.graph.remove_edge(nodes[0], nodes[1])
                else:
                    edges = list(nx.find_cycle(self.graph))
                    edges.remove((nodes[0],nodes[1]))
                    return edges


    def findCycle(self):
        return

    def add_edge(self, v1, v2):
        self.graph.add_edge(v1, v2, weight=distanceBetweenPoints(self.get_node_pos(v1) + (0,), self.get_node_pos(v2) + (0,)))

    def generate_init_tree(self):
        used_nodes = set()
        not_used_nodes = self.cities_nodes
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
            not_used_nodes = self.ps_nodes
            while len(not_used_nodes) != 0:
                node = sample(not_used_nodes, 1)
                node = node.pop(0)
                not_used_nodes.remove(node)
                second_node = sample(used_nodes, 1)
                second_node = second_node.pop(0)
                # remove second_node because one city can be connected with one power station
                used_nodes.remove(second_node)
                self.add_edge(node, second_node)


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

'''class LineSegment:
    def __init__(self, p1, p2, conn=False):
        self.points = set()
        self.points.add(p1)
        self.points.add(p2)
        self.is_conn_to_power = conn

    def __eq__(self, other):
        return self.points == other.points

    def length(self):
        points = self.points.copy()
        return distanceBetweenPoints(points.pop() + (0,), points.pop() + (0,))

    def get_points(self):
        points_copy = self.points.copy()
        return points_copy'''
