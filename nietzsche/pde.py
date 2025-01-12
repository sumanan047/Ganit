"""
PDE class
=========
PDEs that the module should be able to solve are:
1.0 Diffusion as a subclass, this subclass should be able
    to take a space grid and a time grid with some ic and bc
    to solve the problem. 

2.0 Vibration as a subclass,
"""
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt            # plotting the data
import matplotlib.animation as animation   # animation of the plot
from matplotlib.animation import FuncAnimation  # animate a function
from mayavi import mlab
import imageio

from .space import Space
from .time_ import Time
from .utils import Dimension


class PDE:
    """
    Description:
    ============
        General PDE class

    Parameters:
    ============
        about: [str]
            String about the PDE being solved. This
            can be used for reports generated on the solve
        solution_mode: [choice]*
            Choice of:
            - Finite Difference Method [FDM]
            - Finite Element Method [FEM]
        space: [np.ndarray]
            sapce domain, this could be 1D, 2D or 3D
        time: [np.ndarray]
            time domain
    """

    def __init__(self) -> None:
        self.about = None
        self.solution_mode = None
        self.space = None
        self.time = None

    def setup(self):
        pass

    def solve(self):
        pass

    def export(self):
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
        """
        Description:
        ============
            Sets the time step for the simulation.

        Parameters:
        ============
            None

        Returns:
        ============
            None

        Example:
        ============
        >>> ti = Time()
        >>> ti.set_dt()  # set the dt value for the time object
        """
        if self.time is not None:
            self.dt = self.time[1] - self.time[0]
        else:
            raise ValueError(f'dt for simulation was not set correctly')
        return None

    def set_primal_domain(self, space_array, time_array):
        """
        Description:
        ============
            Sets the primal field of the variable that diffuses over time and
            space in the simulation. Primal domain is the space domain,
            but we attach it to the pde solution scheme. We put the shape as 
            numpy array shape (time, x, y, z, . .)

        Parameters:
        ============
            space_object: np.ndarry
                space parameter to be used in the diffusion simulation.
                This is obtained after using the space.setup method
            time_object: np.ndarray
                time parameter to be used in the diffusion simulation.
                This is obtained after using the time.setup method

        Returns:
        ============
            None
            But it sets the primal domain for the simulation
            self.primal_domain is set to be a numpy array of the primal domain
            with zeros filled in with shapes given as follwing in diffferent
            dimensions:
            - 1D: time, space
            - 2D: time, space[0], space[1]
            - 3D: time, space[0], space[1], space[2]

        Example:
        ============
            >>> # set space
            >>> s = Space()
            >>> s.dimension = Dimension.DD.value # DD for 2D
            >>> l = s.setup()
            >>> x = l[0]
            >>> y = l[1]
            >>> # set time
            >>> time = Time()
            >>> t = time.setup()
            >>> # set diffusion
            >>> diff = Diffusion()
            >>> diff.set_primal_domain(space_object=x,time_object=t)
            >>> diff.primal_domain
        """
        self.space = space_array
        self.time = time_array
        self.set_dt()  # set the dt value for the simulation
        if len(self.space) == 1:
            self.primal_domain = np.zeros([len(self.time), len(self.space[0])])
        elif len(self.space) == 2:
            self.primal_domain = np.zeros(
                [len(self.time), len(self.space[0]), len(self.space[1])])
        elif len(self.space) == 3:
            self.primal_domain = np.zeros(
                [len(self.time),
                 len(self.space[0]),
                 len(self.space[1]),
                 len(self.space[2])])
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
        >>> diff.set_primal_domain(space_array=x,time_array=t)
        >>> diff.boundary_condition(constant_value=1.0)
        """
        # start the whole domain with a constant value
        new_primal_domain = np.full(primal_domain.shape, constant_value)
        if primal_domain.ndim == 2:
            # iterate over the time axis i.e., new_primal_domain.shape[0]
            for i in range(new_primal_domain.shape[0]):
                new_primal_domain[i,
                                  thickness:-thickness] = primal_domain[i,
                                                                        thickness:-thickness]
        elif primal_domain.ndim == 3:
            # iterate over the time axis i.e., new_primal_domain.shape[0]
            for i in range(new_primal_domain.shape[0]):
                new_primal_domain[i, thickness:-thickness,
                                  thickness:-thickness] = primal_domain[i,
                                                                        thickness:-thickness,
                                                                        thickness:-thickness]

        elif primal_domain.ndim == 4:
            # iterate over the time axis i.e, new_primal_domain.shape[0]
            for i in range(new_primal_domain.shape[0]):
                new_primal_domain[i, thickness:-thickness,
                                  thickness:-thickness,
                                  thickness:-thickness] = primal_domain[i, thickness:-thickness,
                                                                        thickness:-thickness,
                                                                        thickness:-thickness]
        return new_primal_domain

    def initial_condition(self,
                          general_value: float,
                          specific_value: float,
                          x_ilocation,
                          x_elocation,
                          y_ilocation,
                          y_elocation,
                          z_ilocation,
                          z_elocation):
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
        >>> diff.set_primal_domain(space_array=x,time_array=t)
        >>> diff.boundary_condition(constant_value=1.0)
        """
        if self.primal_domain is not None:
            self.primal_domain[0].fill(general_value)
            if self.primal_domain.ndim == 2:
                self.primal_domain[:, x_ilocation:x_elocation] = specific_value
            elif self.primal_domain.ndim == 3:
                self.primal_domain[0,
                                   x_ilocation:x_elocation,
                                   y_ilocation:y_elocation] = specific_value
            elif self.primal_domain.ndim == 4:
                self.primal_domain[0,
                                   x_ilocation:x_elocation,
                                   y_ilocation:y_elocation,
                                   z_ilocation:z_elocation] = specific_value
        else:
            raise ValueError('Could not set primal domain correctly!')
        return None

    def solve(self, step_constant):
        """
        Description:
        =============
            This does an explicit marching in time to estimate the pressure
            domain in the homogenoeus scheme.

        Parameters:
        =============
            step_constant: [float]
                The constant value of the primal domain in general

        Returns:
        =============
            None

        Example:
        =============
        >>> # set diffusion
        >>> diff = Diffusion()
        >>> diff.set_primal_domain(space_object=x,time_object=t)
        >>> diff.boundary_condition(constant_value=1.0)
        >>> diff.solve(0.1)
        """
        if self.space is not None and self.time is not None:
            if len(self.space) == 1:
                for k in range(0, len(self.time)-1, 1):
                    for i in range(1, len(self.space[0])-1):
                        self.primal_domain[k + 1, i] = step_constant * (self.primal_domain[k][i+1] + self.primal_domain[k][i-1] -
                                                                        2*self.primal_domain[k][i]) + self.primal_domain[k][i]
            elif len(self.space) == 2:
                for k in range(0, len(self.time)-1, 1):
                    for i in range(1, len(self.space[0])-1):
                        for j in range(1, len(self.space[1])-1):
                            # print(self.primal_domain)
                            self.primal_domain[k + 1, i, j] = step_constant * (self.primal_domain[k][i+1][j] + self.primal_domain[k][i-1][j] +
                                                                               self.primal_domain[k][i][j+1] + self.primal_domain[k][i][j-1] -
                                                                               4*self.primal_domain[k][i][j]) + self.primal_domain[k][i][j]
            elif len(self.space) == 3:
                for l in range(0, len(self.time)-1, 1):
                    for k in range(0, len(self.space[0])-1):
                        for i in range(1, len(self.space[1])-1):
                            for j in range(1, len(self.space[2])-1):
                                self.primal_domain[l + 1, k, i, j] = step_constant * (self.primal_domain[l][k][i+1][j] + self.primal_domain[l][k][i-1][j] +
                                                                                      self.primal_domain[l][k][i][j+1] + self.primal_domain[l][k][i][j-1] +
                                                                                      self.primal_domain[l][k+1][i][j] + self.primal_domain[l][k-1][i][j] -
                                                                                      6*self.primal_domain[l][k][i][j]) + self.primal_domain[l][k][i][j]
        else:
            raise ValueError(
                "Could not set the space, time or primal domain most likely in the simulation!")
        return None

    def export_result(self):
        if self.primal_domain.ndim == 2:
            df = pd.DataFrame(self.primal_domain[:,:], index = self.time)
            df.to_csv('results.csv')
        else:
            with h5py.File('finite_difference_results.h5', 'w') as hf:
                hf.create_dataset('data', data=self.primal_domain)
                hf.create_dataset('time', data=self.time)
                hf.create_dataset('space', data=self.space)


    def diffusion_heatmap(self, pk, k):
        """
        Description:
        ============
            Function that plots the heatmap of the pressure domain at a specific time

        Parameters:
        ============
            pk
            k

        Returns:
        ============
            None

        Example:
        ============
        >>> # set diffusion
        >>> diff = Diffusion()
        >>> diff.set_primal_domain(space_object=x,time_object=t)
        >>> diff.boundary_condition(constant_value=1.0)
        >>> diff.solve(0.1)
        >>> diff.diffusion_heatmap(diff.primal_domain[k],k)
        """
        # Clear the current plot figure
        plt.clf()
        plt.title(f"Pressure at time = {k*self.dt:.1f} unit time")
        plt.xlabel("Easting")
        plt.ylabel("Northing")

        # This is to plot u_k (u at time-step k)
        if self.primal_domain is not None:
            # ndim is 2 when time, x i.e. a 1D problem
            if self.primal_domain.ndim == 2:
                y_lims = []
                for i in range(self.primal_domain.shape[0]):
                    y_ = max(self.primal_domain[i, :])
                    y_lims.append(y_)
                y_lim = max(y_lims)*1.5
                plt.ylim(0, y_lim)
                plt.plot(self.primal_domain[k])
            elif self.primal_domain.ndim == 3:
                plt.imshow(self.primal_domain[k, :, :])
                plt.colorbar(extend='both')
            elif self.primal_domain.ndim == 4:
                pass
        else:
            raise ValueError("This is not Good man")
        # plt.pcolormesh(self.primal_domain, cmap="coolwarm", vmin=0, vmax=15)
        return plt

    def animate(self, k):
        """
        Description:
        =============
            This sets the animation of the colormap

        Parameters:
        =============
            k: [int]
                time step

        Returns:
        =============
            None

        Example:
        =============
        >>> # set diffusion
        >>> diff = Diffusion()
        >>> diff.set_primal_domain(space_object=x,time_object=t)
        >>> diff.boundary_condition(constant_value=1.0)
        >>> diff.solve(0.1)
        >>> diff.animate(k)
        """
        if self.primal_domain is not None:
            self.diffusion_heatmap(self.primal_domain[k], k)
        else:
            raise ValueError(f'Could not set the primal domain!')

    def visualize(self):
        pass
