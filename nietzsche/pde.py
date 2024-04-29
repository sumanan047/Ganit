"""
PDE class and that has 

PDEs that the module should be able to solve are:

- Diffusion as a subclass, this subclass should be able to take a space grid and a time grid with some ic and bc
to solve the problem. 

- 

"""
import numpy as np
import matplotlib.pyplot as plt
import space
import time


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

    def set_boundary_condition(self, constant_value, thickness=2, mode="Constant"):
        # Create a copy of the domain with the same shape as the domain, filled with the value.
        self.primal_domain = np.full(self.primal_domain.shape, constant_value)
        # Copy the elements from the domain to the new_domain, excluding the outside elements for a given thickness
        self.primal_domain[thickness:-thickness, thickness:-
                           thickness] = self.primal_domain[thickness:-thickness, thickness:-thickness]
        return None

    def set_initial_condition(self, reservoir_pressure, well_pressure):
        self.primal_domain.fill(reservoir_pressure)
        self.primal_domain[0, 20:30, 20:30] = well_pressure
        return None

    def solve(self, step_constant):
        """
        This does an explicit marching in time to estimate the pressure domain in the homogenoeus reservoir.
        """
        for k in range(0, self.time-1, 1):
            for i in range(1, self.space-1):
                for j in range(1, self.space-1):
                    self.primal_domain[k + 1, i, j] = step_constant * (self.primal_domain[k][i+1][j] + self.primal_domain[k][i-1][j] +
                                                                       self.primal_domain[k][i][j+1] + self.primal_domain[k][i][j-1] -
                                                                       4*self.primal_domain[k][i][j]) + self.primal_domain[k][i][j]

        return None

    def reservoir_heatmap(self, pk, k):
        """
        Function that plots the heatmap
        """
        # Clear the current plot figure
        plt.clf()
        plt.title(f"Pressure at time = {k*self.dt:.1f} unit time")
        plt.xlabel("Easting")
        plt.ylabel("Northing")

        # This is to plot u_k (u at time-step k)
        plt.pcolormesh(pk, cmap="coolwarm", vmin=0, vmax=15)
        plt.colorbar()

        return plt

    def animate(self, k):
        """
        This sets the animation of the colormap
        """
        self.reservoir_heatmap(self.primal_domain[k], k)

    def visualize(self):
        pass


s = space.Space()
s.dimension = "3D"
x = s.set()
print(x[1])

# t = Time()
# tp = t.set()
# print(type(tp))
# print(tp[-1])
