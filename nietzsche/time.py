import numpy as np


class Time:
    def __init__(self) -> None:
        self.reletivistic = False

    def set(self, start=0.0, step=100, dt=0.1):
        return np.linspace(start, dt*step, step+1)
