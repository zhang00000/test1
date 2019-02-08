#include <math.h>
#include <stdio.h>
#define PI 3.14159265358979323846

double f(int n, double *x, void *user_data) {
    double c = *(double *)user_data;
    double x0 = x[0];
    double x1 = x[1];
    return c + 0.5 * exp(- x0 * x0 / 2.0 - x1 * x1 / 2.0) / PI;
}

// int main () {
//     double x0 = 0;
//     double x1 = 0;
//     double z = 0.5 / PI * exp(- x0 * x0 / 2.0 - x1 * x1 / 2.0);
//     printf("The exponential value of (%lf, %lf) is %lf\n", x0, x1, z);
//     return(0);
// }
