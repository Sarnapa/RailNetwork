from math import sqrt


def distanceBetweenPoints(point_one, point_two):
    a, b, c = point_one
    x, y, z = point_two
    return sqrt((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2)

