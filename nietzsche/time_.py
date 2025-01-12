import numpy as np

class Time:
    def __init__(self, start:float = 0.0,
                 step:int = 100,
                 dt:float = 0.1,
                 reletivistic=False) -> None:
        self.start = start
        self.step = step
        self.dt = dt
        self.t_arr = np.linspace(self.start, self.dt*self.step, self.step)
        self.reletivistic = reletivistic
