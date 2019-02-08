# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy
from scipy.linalg import block_diag
from scipy.optimize import linprog


def q_solver(v, weight, eps):
    r = numpy.matmul(numpy.diagflat(weight), v)
    c = r.ravel()
    m, n = r.shape
    a_eq = block_diag(*[numpy.ones(n)] * m)
    b_eq = numpy.ones(m)
    b_ub = numpy.zeros(m*(m-1)*n)
    a_ub = numpy.zeros((m * (m-1) * n, m * n))
    r_count = 0
    for j in range(n):
        for k in range(m):
            for i in range(m):
                if k == i:
                    continue
                a_ub[r_count][k*n + j] = 1
                a_ub[r_count][i*n + j] = - numpy.exp(eps)
                r_count += 1
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq)
    return res.x.reshape((m, n)), res.fun
