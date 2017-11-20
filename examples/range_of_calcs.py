from ift import IFT
from objects import *
from equations import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

gamma = 5 / 3
M_e = 2.4
theta_max = prandtl_meyer(M_e, gamma) / 2

decimal = theta_max % 1
integer = theta_max - decimal

# init_thetas = [decimal, integer / 3 + decimal, 2 * integer / 3 + decimal, theta_max]

fig = plt.figure()
fig.patch.set_facecolor('white')
ax = fig.gca()

area_ratios = []
final_ys = []
ns = range(100, 1000, 100)
for n in ns:
    init_thetas = np.logspace(np.log10(1e-2), np.log10(theta_max), n, base=10)
    # init_thetas = np.linspace(1e-2, theta_max, 100)
    np.append(init_thetas, theta_max)

    ift = IFT(1, 3, 0.01, gamma)

    init_points = []
    for theta in init_thetas:
        init_points.append(Point(str(theta), ift, gamma, theta=theta, x=0, y=1, set_all=False))

    internal_points = []
    wall_points = [init_points[-1]]
    symmetry_points = []
    for i in range(len(init_points)):
        init_p = init_points[i]
        init_p.set_M()
        last_p = Point(init_p.pid + "-sym", ift, gamma, b=init_p, y=0)
        symmetry_points.append(last_p)
        for j in range(i + 1, len(init_points)):
            last_p = Point(init_p.pid + "-" + init_points[j].pid, ift, gamma, a=last_p, b=init_points[j])
            internal_points.append(last_p)
        wall_points.append(Point(init_p.pid + "-wall", ift, gamma, b=wall_points[-1], a=last_p, wall=True))

    xs = []
    ys = []
    final_ys.append(wall_points[-1].y)

ratio = area_ratio(M_e, gamma)
ys_plot, = ax.plot(ns, final_ys, 'r', label='MoC final y coordinates')
area_ratios_plot, = ax.plot([ns[0], ns[-1]], [ratio, ratio], 'g--', label="Area ratio")
# ax.plot(xs[-1], area_ratios[-1], 'ro')
# # ax.plot(all_p_xs, all_p_ys, 'gx')  # Show all points.
# ax.annotate("$A/A^{*}$", (xs[-1], area_ratios[-1]), (xs[-1] - 0.6, area_ratios[-1] - 0.2),
#             arrowprops={"arrowstyle": "->"})
# ax.plot(xs, flat, 'r--')  # Change to 'ro' to show point distribution.
ax.set_xlabel(r'Number of initial points', )
ax.set_ylabel(r'$y/r_{a}$')
# ax.axis([2, 100, 1.93, 2.06])
# plt.legend([ys_plot, area_ratios], ['MoC final y coordinates', 'Area ratio'], loc=4)
plt.legend(loc=4)
plt.show()

# print("Area ratio at final point = {0:.3f}".format(area_ratios[-1]))
# print("Final point x coordinate = {0:.3f}".format(xs[-1]))
# print("Final point y coordinate = {0:.3f}".format(ys[-1]))
