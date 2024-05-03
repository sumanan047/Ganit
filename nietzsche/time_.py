import numpy as np


class Time:
    def __init__(self) -> None:
        self.reletivistic = False

    def setup(self, start: float = 0.0, step: int = 100, dt: float = 0.1):
        """
        Description:
        =============
            Sets the time domain with a start, number of steps and then step-size

        Parameters:
        =============
            start: [float]
                starting time with default value of 0.0
            step: [int]
                Number of steps to be involved in the simualtion
            dt: [float]
                step-size in the simulation

        Returns:
        ============
            Numpy array using np.linspace command

        Example:
        ============
            >>> # set time
            >>> time = Time()
            >>> t = time.set()
        """
        return np.linspace(start, dt*step, step)
