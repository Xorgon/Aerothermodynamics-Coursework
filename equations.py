import math


def mach_angle(M, degrees=True):
    rads = math.asin(1. / M)
    if degrees:
        return math.degrees(rads)
    else:
        return rads


def prandtl_meyer(M, gamma, degrees=True):
    g = (gamma + 1.) / (gamma - 1.)
    rads = math.sqrt(g) * math.atan(math.sqrt((M * M - 1.) / g)) - math.atan(math.sqrt(M * M - 1.))
    if degrees:
        return math.degrees(rads)
    else:
        return rads
