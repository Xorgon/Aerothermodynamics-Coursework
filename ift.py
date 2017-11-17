import math
import numpy as np

from equations import *


class IFT:
    table = None

    def __init__(self, M_min, M_max, M_step, gamma):
        self.table = self.generate_ift(M_min, M_max, M_step, gamma)

    def generate_ift(self, M_min, M_max, M_step, gamma):
        table = []
        for M in np.arange(M_min, M_max + 1e-10, M_step):
            table.append([round(M, 4), round(mach_angle(M), 2),
                          round(prandtl_meyer(M, gamma), 2)])
        return table

    def nu_to_M(self, nu):
        for i in range(len(self.table)):
            if self.table[i][2] > nu:
                if i == 0:
                    print("Warning: nu lower than first value in the table.")
                    raise AttributeError
                else:
                    nu_lower = self.table[i - 1][2]
                    nu_upper = self.table[i][2]

                    dif = (nu - nu_lower) / (nu_upper - nu_lower)

                    M_lower = self.table[i - 1][0]
                    M_upper = self.table[i][0]

                    M = M_lower + dif * (M_upper - M_lower)

                    return M
        print("Warning: Value of nu not found in table.")
        return None

    def nu_to_mu(self, nu):
        for i in range(len(self.table)):
            if self.table[i][2] > nu:
                if i == 0:
                    print("Warning: nu lower than first value in the table.")
                    return self.table[i][1]
                else:
                    nu_lower = self.table[i - 1][2]
                    nu_upper = self.table[i][2]

                    dif = (nu - nu_lower) / (nu_upper - nu_lower)

                    mu_lower = self.table[i - 1][1]
                    mu_upper = self.table[i][1]

                    mu = mu_lower + dif * (mu_upper - mu_lower)
                    return mu
        print("Warning: Value of nu not found in table.")
        return None

    def __str__(self):
        out = ""
        for row in self.table:
            line = ""
            for column in row:
                line += "{0:.2f}".format(column)
                line += "," if column != row[-1] else ""
            out += line + "\n"
        return out

# array_to_csv(generate_ift(2.00, 2.20, 0.01, 5 / 3), "Report/argon_ift")
