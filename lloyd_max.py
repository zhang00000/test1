from subgradient import subgradient_2, next_y_from_v
import numpy


def lloyd_max(y0, max_step, eps=0.693147, weight=None):
    y = y0
    for step in range(max_step):
        subgradient_step = 100000 if step == max_step - 1 else 10000
        g, v = subgradient_2(y, subgradient_step, eps, weight)
        y = next_y_from_v(v, y, weight)
        print(step, g)
        print(y)
        history.append((g, y))
    return y


history = []
y_init = numpy.array([[1, 1], [0, 1], [-1, 2]], dtype='float')
lloyd_max(y_init, 10)
