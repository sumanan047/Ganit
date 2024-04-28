"""


Keyword arguments:
argument -- description
Return: return_description
"""


import numpy as np


class PDE:
    pass


class Diffusion(PDE):
    def __init__(self) -> None:
        super().__init__()
        # supposed to contain a description about the PDE class
        self.about = None
        self.solution_mode = "FDM"          # sets the solution mode for the PDE
        self.space = None
        self.time = None
        self.primal_domain = None

    def set_primal_field(self, space_object, time_object):
        self.space = space_object
        self.time = time_object
        if len(self.space) == 1:
            self.primal_domain = np.empty([self.time[-1], self.space[-1]])
        elif len(self.space) == 2:
            self.primal_domain = np.empty(
                [self.time[-1], self.space[0][-1], self.space[1][-1]])
        elif len(self.space) == 3:
            self.primal_domain = np.empty(
                [self.time[-1], self.space[0][-1], self.space[1][-1], self.space[2][-1]])
        else:
            raise ValueError('Could not set the primal field for the solve!')

    def set_boundary_condition(self, domain, constant_value, thickness=2, mode="Constant"):
        # Create a copy of the domain with the same shape as the domain, filled with the value.
        new_domain = np.full(domain.shape, constant_value)
        # Copy the elements from the domain to the new_domain, excluding the outside elements for a given thickness
        new_domain[thickness:-thickness, thickness:-
                   thickness] = domain[thickness:-thickness, thickness:-thickness]
        return new_domain

    def set_initial_condition(self):
        pass

    def solve(self):
        pass

    def visualize(self):
        pass


class Space:
    def __init__(self) -> None:
        self.dimension = "1D"
        self.geometry = "Euclidean"

    def set(self, x_start=0, x_stop=1, x_step=25,
            y_start=0, y_stop=1, y_step=25,
            z_start=0, z_stop=1, z_step=25):
        x = np.linspace(x_start, x_stop, x_step)
        y = np.linspace(y_start, y_stop, y_step)
        z = np.linspace(z_start, z_stop, z_step)
        if self.dimension == "3D":
            return x, y, z
        elif self.dimension == "2D":
            return x, y
        elif self.dimension == "1D":
            return x
        else:
            raise ValueError('Failed to set the space for solution!')


class Time:
    def __init__(self) -> None:
        self.reletivistic = False

    def set(self, start=0.0, step=100, dt=0.1):
        return np.linspace(start, dt*step, step+1)


s = Space()
s.dimension = "3D"
x = s.set()
print(x[1])

# t = Time()
# tp = t.set()
# print(type(tp))
# print(tp[-1])
