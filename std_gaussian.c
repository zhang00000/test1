#include <math.h>
#include <stdio.h>
#define PI 3.14159265358979323846

double f(int n, double *x, void *user_data) {
    double *y = (double *)user_data;
    double x1 = x[0];
    double x0 = x[1];
    double c0 = y[0];
    double c1 = y[1];
    return 0.5 * exp(- (x0 - c0) * (x0 - c0) / 2.0 - (x1 - c1) * (x1 - c1) / 2.0) / PI;
}

double g(int n, double *x, void *user_data) {
    double *y = (double *)user_data;
    double x1 = x[0];
    double x0 = x[1];
    double c0 = y[0];
    double c1 = y[1];
    double y0 = y[2];
    double y1 = y[3];
    return ((x0 - y0) * (x0 - y0) + (x1 - y1) * (x1 - y1)) * 0.5 * exp(- (x0 - c0) * (x0 - c0) / 2.0 - (x1 - c1) * (x1 - c1) / 2.0) / PI;
}

double gx(int n, double *x, void *user_data) {
    double *y = (double *)user_data;
    double x1 = x[0];
    double x0 = x[1];
    double c0 = y[0];
    double c1 = y[1];
    return x0 * 0.5 * exp(- (x0 - c0) * (x0 - c0) / 2.0 - (x1 - c1) * (x1 - c1) / 2.0) / PI;
}

double gy(int n, double *x, void *user_data) {
    double *y = (double *)user_data;
    double x1 = x[0];
    double x0 = x[1];
    double c0 = y[0];
    double c1 = y[1];
    return x1 * 0.5 * exp(- (x0 - c0) * (x0 - c0) / 2.0 - (x1 - c1) * (x1 - c1) / 2.0) / PI;
}