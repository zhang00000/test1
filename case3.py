from lloyd_max import lloyd_max
from multiprocessing import Pool
import numpy
import shelve
from scipy.spatial import ConvexHull
from integration_utils import find_coefficients, find_intersections
from subgradient import q_from_v



# def f(y):
#     return lloyd_max(y, 100, subgradient_max_step=1000, eps=0.4)
#
#
# ys = [-2 + 4 * numpy.random.rand(6, 2) for _ in range(5)]
# p = Pool(5)
# optimal = p.map(f, ys)
# with shelve.open('spam') as fh:
#     fh['optimal'] = optimal
#
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


with shelve.open('spam') as fh:
    optimal = fh['optimal']

case = 3

for i in range(100):
    v1 = optimal[case][3][i][2]
    y1 = optimal[case][3][i][1]
    for k in range(2):
        filename1 = f'result3/{i}_{chr(65 + k)}_polygon.txt'
        with open(filename1, 'w') as fh:
            fh.write('group\tx\ty\n')
            for j in range(6):
                poly = gen_polygon(j, k, v1, y1)
                for x, y in poly:
                    fh.write(f'{j}\t{x}\t{y}\n')
    q1 = q_from_v(v1, y1)
    with open(f'result3/{i}_centroids.txt', 'w') as fh1:
        fh1.write('group\tx\ty\tpa\tpb\n')
        for j in range(6):
            fh1.write(f'{j}\t{y1[j, 0]}\t{y1[j, 1]}\t{q1[j, 0]:.2f}\t{q1[j, 1]:.2f}\n')
