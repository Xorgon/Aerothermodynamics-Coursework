import math

from equations import prandtl_meyer, mach_angle


class Point:
    pid = None

    a = None
    b = None
    table_array = None

    gamma = None
    mu = None

    R_plus = None
    R_minus = None

    M = None
    theta = None
    x = None
    y = None

    wall = None

    def __init__(self, pid, table_array, gamma, M=None, theta=None, x=None, y=None, a=None, b=None, R_plus=None,
                 R_minus=None, mu=None, wall=False, set_all=True):

        # Set all required values.
        self.pid = pid
        self.table_array = table_array
        self.gamma = gamma

        self.wall = wall

        # Set all specified values.
        if theta is not None:
            self.theta = theta
        if M is not None:
            self.M = M
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if a is not None:
            self.a = a
            self.R_plus = a.R_plus
        if b is not None:
            self.b = b
            self.R_minus = b.R_minus
        if R_plus is not None:
            self.R_plus = R_plus
        if R_minus is not None:
            self.R_minus = R_minus
        if mu is not None:
            self.mu = mu

        if x == 0 and theta is not None:
            self.R_minus = 2 * theta  # theta = nu
            self.R_plus = 0

        if M is not None and theta is not None:
            self.R_plus = self.get_nu_from_M() - theta
            self.R_minus = self.get_nu_from_M() + theta

        # Reflection from the centreline.
        if y == 0 and self.b is not None and R_plus is None:
            self.theta = 0  # To satisfy symmetry
            self.R_plus = self.R_minus
            self.a = Point("dummy", self.table_array, self.gamma, theta=-self.b.theta, R_plus=self.R_plus,
                           mu=self.b.get_mu(), x=self.b.x, y=-self.b.y, set_all=False)

        if set_all:
            self.set_all()

    def get_nu_from_Rs(self):
        return (self.R_plus + self.R_minus) / 2

    def get_nu_from_M(self):
        return prandtl_meyer(self.M, self.gamma)

    def get_nu(self):
        if self.M is not None:
            return self.get_nu_from_M()
        elif self.R_plus is not None and self.R_minus is not None:
            return self.get_nu_from_Rs()
        else:
            print("Cannot set nu. (id: {0})".format(self.pid))
            return None

    def get_mu(self):
        if self.mu is not None:
            return self.mu
        elif self.R_plus is not None and self.R_minus is not None:
            return self.table_array.nu_to_mu(self.get_nu())
        elif self.M is not None:
            return mach_angle(self.M)
        else:
            print("a is {0}, b is {1}, M is {2}. (id: {3})".format(self.a, self.b, self.M, self.pid))
            raise AttributeError

    def get_alpha_ap(self):
        if not self.wall:
            return 0.5 * (self.a.theta + self.a.get_mu() + self.theta + self.get_mu())
        else:
            return self.a.theta + self.a.get_mu()

    def get_alpha_bp(self):
        if not self.wall:
            return 0.5 * (self.b.theta - self.b.get_mu() + self.theta - self.get_mu())
        else:
            return 0.5 * (self.b.theta + self.a.theta)  # In this case B = previous wall point and theta_A = theta_W

    def set_M(self):
        self.M = self.table_array.nu_to_M(self.get_nu())

    def set_theta(self):
        self.theta = (self.R_minus - self.R_plus) / 2

    def set_x(self):
        tan_alpha_bp = math.tan(math.radians(self.get_alpha_bp()))
        tan_alpha_ap = math.tan(math.radians(self.get_alpha_ap()))
        self.x = (self.b.x * tan_alpha_bp - self.a.x * tan_alpha_ap + self.a.y - self.b.y) \
                 / (tan_alpha_bp - tan_alpha_ap)

    def set_y(self):
        if self.y != 0:
            self.y = self.a.y + (self.x - self.a.x) * math.tan(math.radians(self.get_alpha_ap()))

    def set_Rs(self):
        self.R_plus = self.get_nu() - self.theta
        self.R_minus = self.get_nu() + self.theta

    def set_all(self):
        self.set_M()
        self.set_theta()
        self.set_x()
        self.set_y()
        self.set_Rs()
        return self.M, self.theta, self.x, self.y

    def full_moc_output(self):
        return "{0},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7:.2f},{8:.2f},{9:.2f},{10:.2f}" \
            .format(self.pid, self.R_plus, self.R_minus, self.theta, self.get_nu(), self.M, self.get_mu(),
                    self.theta + self.get_mu(), self.theta - self.get_mu(), self.x, self.y)

    def __str__(self):
        return self.full_moc_output()
