#include <math.h>
#include <stdio.h>
#define PI 3.14159265358979323846

double f(int n, double *x) {
    double x1 = x[0];
    double x0 = x[1];
    return 0.5 * exp(- x0 * x0 / 2.0 - x1 * x1 / 2.0) / PI;
}

double g(int n, double *x, void *user_data) {
    double *y = (double *)user_data;
    double x1 = x[0];
    double x0 = x[1];
    double y0 = y[0];
    double y1 = y[1];
    return ((x0 - y0) * (x0 - y0) + (x1 - y1) * (x1 - y1)) * 0.5 * exp(- x0 * x0 / 2.0 - x1 * x1 / 2.0) / PI;
}
