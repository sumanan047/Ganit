import numpy as np


class Space:
    def __init__(self) -> None:
        self.dimension = "1D"
        self.geometry = "Euclidean"

    def setup(self, x_start=0, x_stop=1, x_step=25,
              y_start=0, y_stop=1, y_step=25,
              z_start=0, z_stop=1, z_step=25):
        """
        Description:
        =============
            Sets the space domain with a start, number of steps and then step-size

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
            Numpy array using np.linspace command

        Example:
        ============
            >>> # set space
            >>> s = Space()
            >>> s.dimension = "2D"
            >>> x = s.setup()
        """
        x = np.linspace(x_start, x_stop, x_step)
        y = np.linspace(y_start, y_stop, y_step)
        z = np.linspace(z_start, z_stop, z_step)
        if self.dimension == "3D":
            return [x, y, z]
        elif self.dimension == "2D":
            return [x, y]
        elif self.dimension == "1D":
            return [x]
        else:
            raise ValueError('Failed to set the space for solution!')
