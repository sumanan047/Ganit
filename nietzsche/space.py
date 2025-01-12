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
    def __init__(self, dimension=Dimension.D.value, geometry="Euclidean",
                 x_start=0,
                 x_stop=1,
                 x_step=25,
                 y_start=0,
                 y_stop=1,
                 y_step=25,
                 z_start=0,
                 z_stop=1,
                 z_step=25) -> None:
        self.dimension = dimension
        self.geometry = geometry
        self.x_start = x_start
        self.x_stop = x_stop
        self.x_step = x_step
        self.y_start = y_start
        self.y_stop = y_stop
        self.y_step = y_step
        self.z_start = z_start
        self.z_stop = z_stop
        self.z_step = z_step
        self.sx = np.linspace(x_start, x_stop, x_step)
        self.sy = np.linspace(y_start, y_stop, y_step)
        self.sz = np.linspace(z_start, z_stop, z_step)
