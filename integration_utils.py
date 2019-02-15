# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 02:03:10 2019

@author: z50
"""

import numpy
from scipy.integrate import dblquad
from scipy.spatial import ConvexHull

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
                    res.append((x, y))
    res1 = numpy.zeros((len(res), 2))
    for i in range(len(res)):
        res1[i, 0] = res[i][0]
        res1[i, 1] = res[i][1]
    return res1


def gen_intervals(j, v, y):
    coefficients = find_coefficients(j, v, y)
    filtered_points = find_intersections(coefficients)
    if len(filtered_points) < 3:
        return None
    hull = ConvexHull(filtered_points)
    x_points = sorted(set(p[0] for p in filtered_points))
    intervals = []
    for x in x_points:
        tp = []
        for i1 in range(len(hull.vertices)):
            i2 = (i1 + 1) % len(hull.vertices)
            x1, x2 = filtered_points[i1, 0], filtered_points[i2, 0]
            y1, y2 = filtered_points[i1, 1], filtered_points[i2, 1]
            if x1 == x:
                tp.append(y1)
            elif (x - x1) * (x - x2) < 0:
                tp.append(y1 + (y2 - y1) * (x - x1) / (x2 - x1))
        tp.sort()
        intervals.append((x, tp[0], tp[-1]))
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
