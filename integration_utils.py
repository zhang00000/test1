# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 02:03:10 2019

@author: z50
"""

from sympy import Point2D
from sympy.geometry import Line, intersection, convex_hull
from scipy.integrate import dblquad


bound = 5


def find_coefficients(j, v, y):
    n = len(v)
    res = [
        (-1, 0, -bound),
        (1, 0, -bound),
        (0, -1, -bound),
        (0, 1, -bound)
    ]
    for i in range(n):
        if i != j:
            a = 2 * (y[i, 0] - y[j, 0])
            b = 2 * (y[i, 1] - y[j, 1])
            c = - y[i, 0] ** 2 + y[j, 0] ** 2 - y[i, 1] ** 2 + y[j, 1] ** 2 - v[j] + v[i]
            res.append((a, b, c))
    return res


def coefficient_to_line(coefficient):
    a, b, c = coefficient
    if b == 0:
        return Line(Point2D(- c / a, 0), Point2D(- c / a, 1))
    else:
        return Line(Point2D(0, - c / b), Point2D(1, (-c - a) / b))


def find_intersections(lines):
    res = []
    for i in range(len(lines)):
        for j in range(i):
            if not lines[i].is_parallel(lines[j]):
                res.append(intersection(lines[i], lines[j])[0])
    return res


def filter_points(points, coefficients):
    res = set()
    for p in points:
        x, y = p.x, p.y
        valid = True
        for coefficient in coefficients:
            a, b, c = coefficient
            if a * x + b * y + c > 1e-8:
                valid = False
        if valid:
            res.add(p)
    return res


def polygon_to_intervals(polygon):
    x_points = sorted(set(p.x for p in polygon.vertices))
    res = []
    for x in x_points:
        vertical_line = Line(Point2D(x, 0), Point2D(x, 1))
        inter = intersection(vertical_line, polygon)
        if len(inter) == 2:
            y1, y2 = sorted(set(p.y for p in inter))
        elif isinstance(inter[0], Point2D):
            y1, y2 = [inter[0].y, inter[0].y]
        else:
            y1, y2 = sorted(set(p.y for p in inter[0].points))
        res.append((x, y1, y2))
    return res


def gen_intervals(j, v, y):
    coefficients = find_coefficients(j, v, y)
    lines = [coefficient_to_line(c) for c in coefficients]
    inter_points = find_intersections(lines)
    filtered_points = filter_points(inter_points, coefficients)
    polygon = convex_hull(*filtered_points)
    intervals = polygon_to_intervals(polygon)
    return intervals


def integrate_over_intervals(interval, func):
    quad = 0.0
    for i in range(1, len(interval)):
        x0, y0, z0 = interval[i-1]
        x1, y1, z1 = interval[i]
        quad += dblquad(
            func, x0, x1,
            lambda x: y0 + (x-x0) * (y1-y0) / (x1-x0),
            lambda x: z0 + (x-x0) * (z1-z0) / (x1-x0),
        )[0]
    return quad
