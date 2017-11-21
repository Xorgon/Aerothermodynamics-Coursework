import solver
from ift import IFT
from equations import *
import matplotlib.pyplot as plt
import numpy as np

gamma = 5 / 3
M_e = 2.4
theta_max = prandtl_meyer(M_e, gamma) / 2
ift = IFT(1, 3, 0.01, gamma)

fig = plt.figure()
fig.patch.set_facecolor('white')
ax = fig.gca()

area_ratios = []
ns = range(4, 100, 1)


def linear(n):
    return np.linspace(1e-2, theta_max, n)


def logarithmic(n):
    return np.logspace(np.log10(1e-2), np.log10(theta_max), n, base=10)


def combo(n):
    return np.sort(
        np.append(np.logspace(np.log10(1e-2), np.log10(theta_max), int(n / 3), base=10),
                  np.linspace(1e-2, theta_max, 2 * int(n / 3))))


dists = [linear, logarithmic, combo]
labels = ["Linear", "Logarithmic", "Combination"]

final_yss = []

for dist in dists:
    final_ys = []
    for n in ns:
        init_thetas = dist(n)

        init_chars, wall_points = solver.solve_min_length_nozzle(init_thetas, M_e, gamma)

        xs = []
        ys = []
        final_ys.append(wall_points[-1].y)
    final_yss.append(final_ys)

ratio = area_ratio(M_e, gamma)
area_ratios_plot, = ax.plot([ns[0], ns[-1]], [ratio, ratio], '--', label="Area ratio")
for i in range(len(dists)):
    print(labels[i] + ": {0:.3f}".format(final_yss[i][-1]))
    ys_plot, = ax.plot(ns, final_yss[i], label=labels[i])
ax.set_xlabel(r'Number of initial points', )
ax.set_ylabel(r'$y/r_{a}$')
ax.axis([2, 100, 1.95, 2.06])
plt.legend(loc=4)
ax.set_title(r"Distributions of initial $\theta s$")
plt.show()
