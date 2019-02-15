import numpy
from integration_utils import gen_intervals, integrate_over_intervals
from scipy import LowLevelCallable
import os, ctypes


def g_w_one_source(v, q, y, pdf, normpdf):
    n = v.size
    w = numpy.zeros(n)
    g = v.dot(q)
    for j in range(n):
        interval = gen_intervals(j, v, y)
        integral1 = integrate_over_intervals(interval, pdf)
        integral2 = integrate_over_intervals(interval, normpdf[j])
        w[j] = q[j] - integral1
        g += integral2 - v[j] * integral1
    return g, w


def subgradient_1(q, y, max_step, pdf, normpdf):
    v = numpy.zeros(len(y))
    v_best = v
    g_best = - numpy.inf
    for step in range(1, max_step):
        g, w = g_w_one_source(v, q, y, pdf, normpdf)
        if g > g_best:
            v_best = v
            g_best = g
        norm = numpy.linalg.norm(w)
        if norm < 1e-8:
            break
        alpha = 1 / step
        v += alpha * w / norm
        print(step, g_best, norm)
    return g_best, v_best


y = numpy.matrix('1 1; 1 -1; -1 1; -1 -1', dtype=float)
q = numpy.array([0.5, 0.2, 0.2, 0.1])

lib = ctypes.CDLL(os.path.abspath('std_gaussian1.so'))
lib.f.restype = ctypes.c_double
lib.f.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double))
p1 = LowLevelCallable(lib.f)
lib.g.restype = ctypes.c_double
lib.g.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
p3 = []
for j in range(len(y)):
    user_data = ctypes.cast(ctypes.pointer((ctypes.c_double*2)(y[j,0], y[j,1])), ctypes.c_void_p)
    p3.append(LowLevelCallable(lib.g, user_data))

subgradient_1(q, y, 20, p1, p3)