# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 02:03:10 2019

@author: z50
"""

from sympy import Point2D
from sympy.geometry import Line, intersection, convex_hull
from scipy.integrate import dblquad

bound = 10.0


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


def find_intersections(coefficients):
    res = []
    for i in range(len(coefficients)):
        L1 = coefficients[i]
        for j in range(i):
            L2 = coefficients[j]
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = - L1[2] * L2[1] + L1[1] * L2[2]
            Dy = - L1[0] * L2[2] + L1[2] * L2[0]
            if D != 0:
                valid = True
                x, y = Dx / D, Dy / D
                for a, b, c in coefficients:
                    if a * x + b * y + c > 1e-8:
                        valid = False
                        break
                if valid:
                    res.append(Point2D(x, y))
    return res


def polygon_to_intervals(polygon):
    x_points = sorted(set(p.x for p in polygon.vertices))
    res = []
    for x in x_points:
        tp = []
        for side in polygon.sides:
            x1, x2, y1, y2 = side.p1.x, side.p2.x, side.p1.y, side.p2.y
            if x1 == x:
                tp.append(y1)
            elif (x - x1) * (x - x2) < 0:
                tp.append(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
        tp.sort()
        res.append((x, tp[0], tp[-1]))
    return res


def gen_intervals(j, v, y):
    coefficients = find_coefficients(j, v, y)
    filtered_points = find_intersections(coefficients)
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
