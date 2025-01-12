import numpy as np
from .utils import Dimension

"""
The Space class produced a space domain for the solution of the PDE.
Eucledean space is the default space domain for the solution of the PDE.
The space domain is set using the setup method which takes the start, stop and step-size
for each dimension.
Setup returns a list of numpy array for each dimension of the space domain in the
order of x, y, z.
"""
class Space:
    def __init__(self, dimension=Dimension.D.value, geometry="Euclidean") -> None:
        self.dimension = dimension
        self.geometry = geometry
        self.sx = None
        self.sy = None
        self.sz = None

    def setup(self, x_start=0, x_stop=1, x_step=25,
              y_start=0, y_stop=1, y_step=25,
              z_start=0, z_stop=1, z_step=25):
        """
        Description:
        =============
            Sets the space domain with a start, number of steps and then step-size.
            This method is mart, it will pick up the cirrect dimension of the space if
            you have set the dimension.

        Parameters:
        =============
            x_start: [float]
                Starting position in x direction with default value of 0.0
            x_stop: [float]
                Final position in x direction with default value of 1.0
            x_step: [int]
                step-size in the x direction
            y_start: [float]
                Starting position in y direction with default value of 0.0
            y_stop: [float]
                Final position in x direction with default value of 1.0
            y_step: [int]
                step-size in the y direction
            z_start: [float]
                Starting position in z direction with default value of 0.0
            z_stop: [float]
                Final position in x direction with default value of 1.0
            z_step: [int]
                step-size in the z direction

        Returns:
        ============
            List of numpy array using np.linspace

        Example:
        ============
            >>> # set space
            >>> s = Space()
            >>> s.dimension = Dimension.DD.value # DD for 2D
            >>> x = s.setup()
        """
        self.sx = np.linspace(x_start, x_stop, x_step)
        self.sy = np.linspace(y_start, y_stop, y_step)
        self.sz = np.linspace(z_start, z_stop, z_step)
        if self.dimension == 3:
            return [self.sx, self.sy, self.sz]
        elif self.dimension == 2:
            return [self.sx, self.sy]
        elif self.dimension == 1:
            return [self.sx]
        else:
            raise ValueError('Failed to set the space for solution!')
