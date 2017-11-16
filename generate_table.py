# -*- coding: utf-8 -*-
"""
Aerothermodynamics Coursework Assignment

@author: Elijah Andrews
"""

import math
import numpy as np


def mach_angle(M, degrees=True):
    rads = math.asin(1. / M)
    if degrees:
        return math.degrees(rads)
    else:
        return rads


def prandtl_meyer(M, gamma, degrees=True):
    g = (gamma + 1.) / (gamma - 1.)
    rads = math.sqrt(g) * math.atan(math.sqrt((M * M - 1.) / g)) \
           - math.atan(math.sqrt(M * M - 1.))
    if degrees:
        return math.degrees(rads)
    else:
        return rads


def generate_ift(M_min, M_max, M_step, gamma, degrees=True):
    table = []
    for M in np.arange(M_min, M_max + 1e-10, M_step):
        table.append([round(M, 4), round(mach_angle(M), 2),
                      round(prandtl_meyer(M, gamma), 2)])
    return table


def array_to_csv(array, filename, header=None):
    f = open(filename + ".csv", 'w')
    if header is not None:
        f.write(header + "\n")
    for row in array:
        line = ""
        for column in row:
            line += "{0:.2f}".format(column)
            line += "," if column != row[-1] else ""
        f.write(line + "\n")
    f.close()


array_to_csv(generate_ift(2.00, 2.20, 0.01, 5 / 3), "Report/argon_ift")
