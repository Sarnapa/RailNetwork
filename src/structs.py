
class RailNetworkTree:

    def __init__(self):
        self.cities_segments = []
        self.city_power_segments = []
        self.score = 0

    def count_score(self, rail_cost, power_lines_cost):
        self.score = 0
        #so far
        for seg in self.cities_segments:
            self.score += seg.length() * rail_cost

        for seg in self.city_power_segments:
            self.score += seg.length() * power_lines_cost

        self.score = 1.0 / self.score
        return self.score

    def add_new_segment(self, line_segment):
        self.segments.append(line_segment)


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
        return distance(points.pop() + (0,), points.pop() + (0,))

    def get_points(self):
        points_copy = self.points.copy()
        return points_copy

    def get_is_conn_to_power(self):
        return self.is_conn_to_power
