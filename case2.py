from case1 import step_size1
from lloyd_max import lloyd_max
from multiprocessing import Pool
import numpy
import shelve
from scipy.spatial import ConvexHull
from integration_utils import find_coefficients, find_intersections
from subgradient import q_from_v


epss = [0, 0.2, 0.4, 0.6, 1]
y = numpy.array([
    [0, -1],
    [-1, 0],
    [1, 0],
    [0, 1]
], dtype=float)


def f(eps):
    return lloyd_max(y, 100, subgradient_max_step=1000, eps=eps)


# p = Pool(1)
optimal = list(map(f, epss))


def gen_polygon(j, k, v, y):
    coefficients = find_coefficients(j, v[:, k], y, bound=2.5)
    filtered_points = find_intersections(coefficients)
    polygon = []
    if len(filtered_points) < 3:
        return polygon
    hull = ConvexHull(filtered_points)
    for index in hull.vertices:
        polygon.append(filtered_points[index])
    return polygon


# with shelve.open('spam') as fh:
#     res4 = fh['3'][3]
#
# for step in range(30):
#     v1 = res4[step][2]
#     y1 = res4[step][1]
#     for k in range(2):
#         filename1 = f'result3/{step}_{chr(65 + k)}_polygon.txt'
#         with open(filename1, 'w') as fh:
#             fh.write('group\tx\ty\n')
#             for j in range(4):
#                 poly = gen_polygon(j, k, v1, y1)
#                 for x, y in poly:
#                     fh.write(f'{j}\t{x}\t{y}\n')
#     with open(f'result3/{step}_centroids.txt', 'w') as fh1:
#         fh1.write('group\tx\ty\n')
#         for j in range(4):
#             fh1.write(f'{j}\t{y1[j, 0]}\t{y1[j, 1]}\n')


for i in range(5):
    v1 = optimal[i][2]
    y1 = optimal[i][1]
    for k in range(2):
        filename1 = f'result4/{i}_{chr(65 + k)}_polygon.txt'
        with open(filename1, 'w') as fh:
            fh.write('group\tx\ty\n')
            for j in range(4):
                poly = gen_polygon(j, k, v1, y1)
                for x, y in poly:
                    fh.write(f'{j}\t{x}\t{y}\n')
    q1 = q_from_v(v1, y1)
    with open(f'result4/{i}_centroids.txt', 'w') as fh1:
        fh1.write('group\tx\ty\tpa\tpb\n')
        for j in range(4):
            fh1.write(f'{j}\t{y1[j, 0]}\t{y1[j, 1]}\t{q1[j, 0]:.2f}\t{q1[j, 1]:.2f}\n')
