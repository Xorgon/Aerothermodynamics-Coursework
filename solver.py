from objects import *
from ift import IFT
import numpy as np


def solve_min_length_nozzle(M_e, gamma, n=100, init_thetas=None):
    """
    Calculates the minimum length of a nozzle for a given M_e and gamma.

    :param M_e: Design exit Mach number of the nozzle.

    :param gamma: Gamma value for the operating fluid.

    :param n: Number of initial theta values to use (default=100).

    :param init_thetas: Initial theta values to use (default is a combination linear/logarithmic distribution).

    :return: initial characteristic lines objects, wall point objects.
    """
    if M_e > 5:
        raise ValueError("M_e is out of the IFT range. (M_e must be less than 5)")

    theta_max = prandtl_meyer(M_e, gamma) / 2
    if init_thetas is not None and max(init_thetas) > theta_max:
        raise ValueError("Maximum theta value is higher than theta_max for given M_e.")
    if init_thetas is None:
        init_thetas = np.sort(np.append(np.logspace(np.log10(1e-2), np.log10(theta_max), int(n / 3), base=10),
                                        np.linspace(1e-2, theta_max, 2 * int(n / 3))))

    ift = IFT(1, 5, 0.01, gamma)

    init_thetas = np.sort(init_thetas)  # Ensure initial thetas are in order.
    init_chars = []
    for theta in init_thetas:
        init_chars.append(
            InitChar(str(theta), Point(str(theta) + "-init", ift, gamma, theta=theta, x=0, y=1, set_all=False)))

    for init_char in init_chars:
        init_char.points[0].set_M()

    wall_points = [init_chars[-1].points[0]]
    for i in range(len(init_chars)):
        init_char = init_chars[i]
        last_p = init_char.add_point(Point(init_char.cid + "-sym", ift, gamma, b=init_char.get_last(), y=0))
        for j in range(i + 1, len(init_chars)):
            cross_char = init_chars[j]
            last_p = Point(init_char.cid + "-" + cross_char.cid, ift, gamma, a=last_p, b=cross_char.get_last())
            init_char.add_point(last_p)
            cross_char.add_point(last_p)
        wall_points.append(
            init_char.add_point(Point(init_char.cid + "-wall", ift, gamma, b=wall_points[-1], a=last_p, wall=True)))

    return init_chars, wall_points
