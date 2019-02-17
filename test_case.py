import numpy
from lloyd_max import lloyd_max
import sys


def step_size1(step):
    if step <= 100:
        return 1/step ** 0.5
    else:
        return step_size1(100) * 0.9 ** (step - 100)


def test(eps, n):
    def f(y):
        return lloyd_max(y, 30, subgradient_max_step=200, step_size_func=step_size1, eps=eps)[0]
    ys = [-2 + 4 * numpy.random.rand(n, 2) for _ in range(5)]
    res = map(f, ys)
    return min(res)


def dummy(eps, n):
    return eps + n


if __name__ == '__main__':
    eps = sys.argv[1]
    n = sys.argv[2]

    result = str(test(float(eps), int(n)))
    filename = f'res_{n}_{eps}.txt'
    with open(filename, 'w') as fh:
        fh.write(f'{n}\t{eps}\t{result}\n')
#
# ns = [2, 3, 4, 5, 6, 7, 8, 9, 10]
# epsilons = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
