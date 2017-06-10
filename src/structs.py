from src.utils import distanceBetweenPoints
from random import sample
import networkx as nx


class RailNetworkTree:

    def __init__(self, pos_dict: dict):
        self.graph = nx.Graph()
        for vertex, pos in pos_dict.items():
            self.graph.add_node(vertex, x=pos[0], y=pos[1])
            print(vertex, end=" ")
            print(self.get_node_x(vertex), end=" ")
            print(self.get_node_y(vertex))

    def get_node_x(self, vertex):
        return self.graph.node[vertex]['x']

    def get_node_y(self, vertex):
        return self.graph.node[vertex]['y']

    '''
    def count_score(self, rail_cost, power_lines_cost):
        self.score = 0
        #so far
        for seg in self.cities_segments:
            self.score += seg.length() * rail_cost

        for seg in self.city_power_segments:
            self.score += seg.length() * power_lines_cost

        self.score = 1.0 / self.score
        return self.score

    def add_new_segment(self, line_segment: LineSegment):
        if line_segment.is_conn_to_power:
            self.city_power_segments.append(line_segment)
        else:
            self.cities_segments.append(line_segment)

    # to random one segment to get cycle
    def random_new_segment(self):
        insert_point = None
        out_points = None
        new_segment = None
        neighbours_list = self.to_neighbours_list()
        all_points = set(neighbours_list.keys())
        unchosen_points = all_points.copy()
        while unchosen_points:
            insert_point = sample(unchosen_points, 1).pop()
            unchosen_points.remove(insert_point)
            neighbour_points = neighbours_list[insert_point]
            out_points = (all_points - neighbour_points)
            out_points.remove(insert_point)
            if out_points:
                break

        # if there are some no "neighbour point", we create new segment.
        if out_points:
            new_neighbour = sample(out_points, 1).pop()
            new_segment = LineSegment(insert_point, new_neighbour)
            self.add_new_segment(new_segment)
        else:
            pass

        return new_segment

    # to create neighbours list that contains all neighbours for one index
    def to_neighbours_list(self):
        neighbours_list = {}
        for seg in self.cities_segments:
            points = seg.points.copy()
            point1 = points.pop()
            point2 = points.pop()
            if point1 not in neighbours_list:
                neighbours_list[point1] = set()
            if point2 not in neighbours_list:
                neighbours_list[point2] = set()
            neighbours_list[point1].add(point2)
            neighbours_list[point2].add(point1)
        return neighbours_list

    def find_cycle(self):
        G = nx.Graph
        nx.find_cycle()

        return cycle

    def get_cities_edges_list(self):
        cities_edges_list = []
        for seg in self.cities_segments:
            points = seg.points.copy()
            cities_edges_list.append(points)

        return cities_edges_list
    '''

class LineSegment:

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
        return points_copy
