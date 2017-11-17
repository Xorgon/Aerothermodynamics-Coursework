from ift import IFT
from objects import *
from equations import *
import matplotlib.pyplot as plt
import numpy as np

gamma = 5 / 3
M_e = 2.4
theta_max = prandtl_meyer(M_e, gamma) / 2

decimal = theta_max % 1
integer = theta_max - decimal

# init_thetas = [decimal, integer / 3 + decimal, 2 * integer / 3 + decimal, theta_max]

init_thetas = np.arange(0.01, theta_max, 0.01)
np.append(init_thetas, theta_max)

ift = IFT(1, 3, 0.01, gamma)

init_points = []
for theta in init_thetas:
    init_points.append(Point(str(theta), ift, gamma, theta=theta, x=0, y=1, set_all=False))

wall_points = [init_points[-1]]
for i in range(len(init_points)):
    init_p = init_points[i]
    last_p = Point(init_p.pid + "-sym", ift, gamma, b=init_p, y=0)
    for j in range(i + 1, len(init_points)):
        last_p = Point(init_p.pid + "-" + init_points[j].pid, ift, gamma, a=last_p, b=init_points[j])
    wall_points.append(Point(init_p.pid + "-wall", ift, gamma, b=wall_points[-1], a=last_p, wall=True))

xs = []
ys = []
for p in wall_points:
    xs.append(p.x)
    ys.append(p.y)

plt.plot(xs, ys)
plt.show()
