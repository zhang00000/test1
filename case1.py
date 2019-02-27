import numpy
from lloyd_max import lloyd_max
from multiprocessing import Pool
from functools import partial


def find_minimal_distortion(eps, n):
    def f(y):
        return lloyd_max(y, 30, subgradient_max_step=1000, eps=eps)[0]
    ys = [-2 + 4 * numpy.random.rand(n, 2) for _ in range(4)]
    res = map(f, ys)
    return min(res)


if __name__ == '__main__':
    epsilons = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for n in range(2, 7):
        p_func = partial(find_minimal_distortion, n=n)
        p = Pool(6)
        results = p.map(p_func, epsilons)
        for eps, result in zip(epsilons, results):
            filename = f'res_{n}_{eps}.txt'
            with open(filename, 'w') as fh:
                fh.write(f'{n}\t{eps}\t{result}\n')
