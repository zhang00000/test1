import numpy
from integration_utils import gen_intervals, integrate_over_intervals


def w_one_source(v, q, y, p):
    n = v.size
    w = numpy.zeros(n)
    for j in range(n):
        interval = gen_intervals(j, v, y)
        w[j] = q[j] - integrate_over_intervals(interval, p)
    return w


p1 = lambda x, y: 0.5 / numpy.pi * numpy.exp(-x**2/2 - y**2/2)
v = numpy.array([0, 0, 2])
y = numpy.matrix('1 0; 0 1; -1 0')
q = numpy.array([0.1, 0.3, 0.6])
res = w_one_source(v, q, y, p1)
print(res)
