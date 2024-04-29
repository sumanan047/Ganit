import numpy as np


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
