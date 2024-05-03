"""
PDE class and that has 

PDEs that the module should be able to solve are:

- Diffusion as a subclass, this subclass should be able to take a space grid and a time grid with some ic and bc
to solve the problem. 

- 

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  # animation of the plot
from matplotlib.animation import FuncAnimation  # animate a function
from space import Space
from time_ import Time


class PDE:
    def __init__(self) -> None:
        pass

    def setup(self):
        pass

    def solve(self):
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
        self.dt = None

    def set_dt(self):
        if self.time is not None:
            self.dt = self.time[1] - self.time[0]
        else:
            raise ValueError(f'dt for simulation was not set correctly')
        return None

    def set_primal_domain(self, space_object, time_object):
        """
        Description:
        ============
            Sets the primal field of the variable that diffuses over time and space in the simulation.

        Parameters:
        ============
            space_object: np.ndarry
                space parameter to be used in the diffusion simulation. This is obtained after using the space.setup method
            time_object: np.ndarray
                time parameter to be used in the diffusion simulation. This is obtained after using the time.setup method

        Returns:
        ============
            Primary field or domain.
        """
        self.space = space_object
        self.time = time_object
        self.set_dt()  # set the dt value for the simulation
        if len(self.space) == 1:
            self.primal_domain = np.zeros([len(self.time), len(self.space[0])])
        elif len(self.space) == 2:
            self.primal_domain = np.zeros(
                [len(self.time), len(self.space[0]), len(self.space[1])])
        elif len(self.space) == 3:
            self.primal_domain = np.zeros(
                [len(self.time), len(self.space[0]), len(self.space[1]), len(self.space[2])])
        else:
            raise ValueError('Could not set the primal field for the solve!')

    @staticmethod
    def boundary_condition(primal_domain, constant_value, thickness=2, mode="Constant"):
        """
        Description:
        =============
            Sets the boundary condition to a constant value at the boundary of the domain

        Parameters:
        =============
            constant_value: [float]
                The constant value of the primal domain at the boundary
            thickness: [int]
                The number of cells from the boundary that should be set to the constant value
            mode: [str]
                It is set to constant for now
                #TODO: Think of other implementation

        Returns:
        =============
            None

        Example:
        =============
        >>> # set diffusion
        >>> diff = Diffusion()
        >>> diff.set_primal_domain(space_object=x,time_object=t)
        >>> diff.boundary_condition(constant_value=1.0)
        """
        new_primal_domain = np.full(primal_domain.shape, constant_value)
        for i in range(new_primal_domain.shape[0]):
            new_primal_domain[i, thickness:-thickness, thickness:-
                              thickness] = primal_domain[i, thickness:-thickness, thickness:-thickness]
        return new_primal_domain

    def initial_condition(self, general_value: float, specific_value: float):
        """
        Description:
        =============
            Sets the initial condition within a domain with a general value throughout the domain
            and then specific value at a specific place in the domain.

        Parameters:
        =============
            general_value: [float]
                The constant value of the primal domain in general
            specific_value: [int]
                The constant value at a speicific place in the primal domain
            #TODO: put loaction feature here
            location: [np.ndarray]
                location in the primal domain where the specific value would be set

        Returns:
        =============
            None

        Example:
        =============
        >>> # set diffusion
        >>> diff = Diffusion()
        >>> diff.set_primal_domain(space_object=x,time_object=t)
        >>> diff.boundary_condition(constant_value=1.0)
        """
        if self.primal_domain is not None:
            self.primal_domain[0].fill(general_value)
            self.primal_domain[0, 2:3, 2:3] = specific_value
        else:
            raise ValueError('Could not set primal domain correctly!')
        return None

    def solve(self, step_constant):
        """
        This does an explicit marching in time to estimate the pressure domain in the homogenoeus reservoir.
        """
        if self.space is not None and self.time is not None:
            print(len(self.space[0]))
            for k in range(0, len(self.time)-1, 1):
                for i in range(1, len(self.space[0])-1):
                    for j in range(1, len(self.space[1])-1):
                        # print(self.primal_domain)
                        self.primal_domain[k + 1, i, j] = step_constant * (self.primal_domain[k][i+1][j] + self.primal_domain[k][i-1][j] +
                                                                           self.primal_domain[k][i][j+1] + self.primal_domain[k][i][j-1] -
                                                                           4*self.primal_domain[k][i][j]) + self.primal_domain[k][i][j]
        else:
            raise ValueError(
                "Could not set the space, time or primal domain most likely in the simulation!")
        return None

    def diffusion_heatmap(self, pk, k):
        """
        Function that plots the heatmap
        """
        # Clear the current plot figure
        plt.clf()
        plt.title(f"Pressure at time = {k*self.dt:.1f} unit time")
        plt.xlabel("Easting")
        plt.ylabel("Northing")

        # This is to plot u_k (u at time-step k)
        if self.primal_domain is not None:
            plt.imshow(self.primal_domain[k, :, :])
        else:
            raise ValueError("This is not Good man")
        # plt.pcolormesh(self.primal_domain, cmap="coolwarm", vmin=0, vmax=15)
        plt.colorbar()
        return plt

    def animate(self, k):
        """
        This sets the animation of the colormap
        """
        if self.primal_domain is not None:
            self.diffusion_heatmap(self.primal_domain[k], k)
        else:
            raise ValueError(f'Could not set the primal domain!')

    def visualize(self):
        pass


if __name__ == "__main__":
    # implementation
    # set space
    s = Space()
    s.dimension = "2D"
    dd_space = s.setup(x_step=60, y_step=60)

    # set time
    tt = Time()
    t = tt.setup(step=5000)

    # set diffusion
    diff = Diffusion()
    diff.set_primal_domain(space_object=dd_space, time_object=t)
    diff.initial_condition(general_value=15.0, specific_value=0.00)
    diff.primal_domain = diff.boundary_condition(
        diff.primal_domain, constant_value=2.0, thickness=1)
    diff.solve(0.1)
    # for i in range(diff.primal_domain.shape[0]):
    # plot_array(diff.primal_domain[i,:,:])
    anim = animation.FuncAnimation(
        plt.figure(), diff.animate, interval=1, frames=len(t), repeat=False)
    anim.save("2D-heat_equation_solution.gif")
