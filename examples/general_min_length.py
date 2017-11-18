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

init_thetas = np.logspace(np.log10(1e-2), np.log10(theta_max), 100, base=10)
np.append(init_thetas, theta_max)

ift = IFT(1, 3, 0.01, gamma)

init_points = []
for theta in init_thetas:
    init_points.append(Point(str(theta), ift, gamma, theta=theta, x=0, y=1, set_all=False))

wall_points = [init_points[-1]]
for i in range(len(init_points)):
    init_p = init_points[i]
    init_p.set_M()
    last_p = Point(init_p.pid + "-sym", ift, gamma, b=init_p, y=0)
    for j in range(i + 1, len(init_points)):
        last_p = Point(init_p.pid + "-" + init_points[j].pid, ift, gamma, a=last_p, b=init_points[j])
    wall_points.append(Point(init_p.pid + "-wall", ift, gamma, b=wall_points[-1], a=last_p, wall=True))

xs = []
ys = []
area_ratios = []
for p in wall_points:
    xs.append(p.x)
    ys.append(p.y)
    area_ratios.append(area_ratio(p.M, gamma))

flat = []
for x in xs:
    flat.append(0)

# plt.plot(xs, ys, xs, flat, 'r--')
# plt.show()

fig = plt.figure()
fig.patch.set_facecolor('white')
ax = fig.gca()
ax.plot(xs, ys)
# ax.plot(xs, area_ratios)
ax.plot(xs, flat, 'r--')  # Change to 'ro' to show point distribution.
ax.set_xlabel(r'$x/r_{a}$', )
ax.set_ylabel(r'$y/r_{a}$')
ax.axis([0, xs[-1], -0.1, ys[-1] + 0.1])
# plt.legend([explicit_avgs_plot, implicit_avgs_plot], ['Explicit', 'Implicit'], loc=4)
plt.show()
