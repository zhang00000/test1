import numpy
import os, ctypes
from scipy import LowLevelCallable
from integration_utils import gen_intervals, integrate_over_intervals
from q_solver import q_solver

center = numpy.array([[-1, 0], [1, 0]])

lib = ctypes.CDLL(os.path.abspath('std_gaussian.so'))
lib.f.restype = ctypes.c_double
lib.f.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.g.restype = ctypes.c_double
lib.g.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.gx.restype = ctypes.c_double
lib.gx.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.gy.restype = ctypes.c_double
lib.gy.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)


def gen_pdf(label):
    user_data = ctypes.cast(
        ctypes.pointer((ctypes.c_double * 2)(center[label, 0], center[label, 1])),
        ctypes.c_void_p
    )
    return LowLevelCallable(lib.f, user_data)


def gen_norm_pdf(label, yj):
    user_data = ctypes.cast(
        ctypes.pointer((ctypes.c_double * 4)(center[label, 0], center[label, 1], yj[0], yj[1])),
        ctypes.c_void_p
    )
    return LowLevelCallable(lib.g, user_data)


def gen_x_pdf(label):
    user_data = ctypes.cast(
        ctypes.pointer((ctypes.c_double * 2)(center[label, 0], center[label, 1])),
        ctypes.c_void_p
    )
    return LowLevelCallable(lib.gx, user_data)


def gen_y_pdf(label):
    user_data = ctypes.cast(
        ctypes.pointer((ctypes.c_double * 2)(center[label, 0], center[label, 1])),
        ctypes.c_void_p
    )
    return LowLevelCallable(lib.gy, user_data)


def step_size(step):
    if step < 500:
        return 1/step
    else:
        return 0.002 * 0.99 ** (step - 500)


def g_w_one_source(v, q, y, k):
    n = v.size
    w = numpy.zeros(n)
    g = v.dot(q)
    for j in range(n):
        interval = gen_intervals(j, v, y)
        pdf = gen_pdf(k)
        integral1 = integrate_over_intervals(interval, pdf)
        normpdf = gen_norm_pdf(k, y[j])
        integral2 = integrate_over_intervals(interval, normpdf)
        w[j] = q[j] - integral1
        g += integral2 - v[j] * integral1
    return g, w


def q_from_v(v, y):
    n, m = v.shape
    res = numpy.zeros(y.shape)
    for j in range(n):
        for k in range(m):
            interval = gen_intervals(j, v[:, k], y)
            res[j, k] = integrate_over_intervals(interval, gen_pdf(k))
    return res


def subgradient_1(q, y, max_step, k, step_size_func=step_size):
    v = numpy.zeros(len(y))
    v_best = v
    g_best = - numpy.inf
    for step in range(1, max_step):
        g, w = g_w_one_source(v, q, y, k)
        if g > g_best:
            v_best = v
            g_best = g
        norm = numpy.linalg.norm(w)
        if norm < 1e-8:
            break
        alpha = step_size_func(step)
        v += alpha * w / norm
        print(step, g_best, norm)
    return g_best, v_best


def g_w_multi_source(v, y, eps=0.693147, weight=None):
    n, m = v.shape
    if not weight:
        weight = numpy.ones(m)
    q, g = q_solver(v, weight, eps)
    w = numpy.zeros((n, m))
    for k in range(m):
        for j in range(n):
            interval = gen_intervals(j, v[:, k], y)
            pdf = gen_pdf(k)
            integral1 = integrate_over_intervals(interval, pdf)
            normpdf = gen_norm_pdf(k, y[j])
            integral2 = integrate_over_intervals(interval, normpdf)
            w[j, k] = weight[k] * (q[j, k] - integral1)
            g += weight[k] * (integral2 - v[j, k] * integral1)
    return g, w


def subgradient_2(y, max_step, step_size_func=step_size, eps=0.693147, weight=None, log=False):
    n = len(y)
    m = len(center)
    v = numpy.zeros((n, m))
    v_best = v
    g_best = - numpy.inf
    for step in range(1, max_step + 1):
        g, w = g_w_multi_source(v, y, eps, weight)
        if g > g_best:
            v_best = v
            g_best = g
        norm = numpy.linalg.norm(w)
        if norm < 1e-8:
            break
        alpha = step_size_func(step)
        v += alpha * w / norm
        if log:
            print(step, g_best, norm)
            print(v)
    return g_best, v_best


def next_y_from_v(v, y, weight=None):
    n, m = v.shape
    res = numpy.zeros(y.shape)
    if not weight:
        weight = numpy.ones(m)
    for j in range(n):
        integral_x = numpy.zeros(m)
        integral_y = numpy.zeros(m)
        integral_1 = numpy.zeros(m)
        for k in range(m):
            interval = gen_intervals(j, v[:, k], y)
            integral_x[k] = integrate_over_intervals(interval, gen_x_pdf(k))
            integral_y[k] = integrate_over_intervals(interval, gen_y_pdf(k))
            integral_1[k] = integrate_over_intervals(interval, gen_pdf(k))
        res[j, 0] = integral_x.dot(weight) / integral_1.dot(weight)
        res[j, 1] = integral_y.dot(weight) / integral_1.dot(weight)
    return res


# def g_w_multi_source_3(q, y, eps=0.693147, weight=None):
#     n, m = q.shape
#     if not weight:
#         weight = numpy.ones(m)
#     q, g = q_solver(v, weight, eps)
#     w = numpy.zeros((n, m))
#     for k in range(m):
#         for j in range(n):
#             interval = gen_intervals(j, v[:, k], y)
#             pdf = gen_pdf(k)
#             integral1 = integrate_over_intervals(interval, pdf)
#             normpdf = gen_norm_pdf(k, y[j])
#             integral2 = integrate_over_intervals(interval, normpdf)
#             w[j, k] = weight[k] * (q[j, k] - integral1)
#             g += weight[k] * (integral2 - v[j, k] * integral1)
#     return g, w
#
#
# def subgradient_3(y, max_step, step_size_func=step_size, eps=0.693147, weight=None, log=False):
#     n = len(y)
#     m = len(center)
#     q = numpy.zeros((n, m))
#
#
#     v = numpy.zeros((n, m))
#     v_best = v
#     g_best = - numpy.inf
#     for step in range(1, max_step + 1):
#         g, w = g_w_multi_source(v, y, eps, weight)
#         if g > g_best:
#             v_best = v
#             g_best = g
#         norm = numpy.linalg.norm(w)
#         if norm < 1e-8:
#             break
#         alpha = step_size_func(step)
#         v += alpha * w / norm
#         if log:
#             print(step, g_best, norm)
#             print(v)
#     return g_best, v_best
