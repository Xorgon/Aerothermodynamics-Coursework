# A simple minimum length solution set manually.

from fileio import points_to_csv
from ift import IFT
from objects import *
from equations import *

gamma = 5 / 3
M_e = 2.4
theta_max = prandtl_meyer(M_e, gamma) / 2

decimal = theta_max % 1
integer = theta_max - decimal

initial_thetas = [0.400, (theta_max - 0.400)/3 + 0.4, 2*(theta_max - 0.400)/3 + 0.4, theta_max]
print("Initial Thetas: " + str(initial_thetas))

ift = IFT(1, 3, 0.01, gamma)

p_a = Point("a", ift, gamma, theta=initial_thetas[0], x=0, y=1, set_all=False)
p_b = Point("b", ift, gamma, theta=initial_thetas[1], x=0, y=1, set_all=False)
p_c = Point("c", ift, gamma, theta=initial_thetas[2], x=0, y=1, set_all=False)
p_d = Point("d", ift, gamma, theta=initial_thetas[3], x=0, y=1, set_all=False)

start_points = [p_a, p_b, p_c, p_d]
for p in start_points:
    p.set_M()

p_1 = Point("1", ift, gamma, b=p_a, y=0)
p_2 = Point("2", ift, gamma, a=p_1, b=p_b)
p_3 = Point("3", ift, gamma, b=p_c, a=p_2)
p_4 = Point("4", ift, gamma, b=p_d, a=p_3)
p_5 = Point("5", ift, gamma, b=p_d, a=p_4, wall=True)
p_6 = Point("6", ift, gamma, b=p_2, y=0)
p_7 = Point("7", ift, gamma, b=p_3, a=p_6)
p_8 = Point("8", ift, gamma, b=p_4, a=p_7)
p_9 = Point("9", ift, gamma, b=p_5, a=p_8, wall=True)
p_10 = Point("10", ift, gamma, b=p_7, y=0)
p_11 = Point("11", ift, gamma, b=p_8, a=p_10)
p_12 = Point("12", ift, gamma, b=p_9, a=p_11, wall=True)
p_13 = Point("13", ift, gamma, b=p_11, y=0)
p_14 = Point("14", ift, gamma, b=p_12, a=p_13, wall=True)

propagation_points = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14]

for p in start_points + propagation_points:
    print(p)

points_to_csv("../Report/MoC", start_points + propagation_points)
print("Final point area ratio = {0:.5f}".format(area_ratio(p_14.M, gamma)))
print("Final point area ratio = {0:.5f}".format(area_ratio(M_e, gamma)))
