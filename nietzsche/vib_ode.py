from .time_ import Time
from .space import Space
from .pde import PDE
import numpy as np

class Vibration(PDE):
    def __init__(self, time: Time,
                 space: Space) -> None:
        self.time = time # Time array
        self.space = space # Space array
        self.dimension = space.dimension # Read from space
        self.initial_condition = None # Initial condition
        self.boundary_condition = None # Boundary condition
        self.primal_domain = np.zeros((len(self.time.t_arr), len(self.space.sx), len(self.space.sy), len(self.space.sz))) # Four-dimensional array

    def setup(self, A=0.0, B=1.0, C=0.0):
        """
        Description:
        =============
            Sets the vibration domain with a frequency, amplitude and phase
            u'' + Au' + Bu + C = 0
            with A = 0, B = 1, C = 0
            is the simple harmonic oscillator is,
            u'' + u = 0 is the default solver

        Parameters:
        =============
            A: [float]
                frequency of the vibration
            B: [float]
                Amplitude of the vibration
            C: [float]
                Phase of the vibration
        return None
    """
        

if __name__ == "__main__":
    from .utils import Dimension
    # set time
    t = Time(start = 0.0, step = 100, dt = 0.1)
    t_arr = t.setup()

    # set space
    s = Space(dimension=Dimension.D.value)
    s_arr = s.setup(start=0, stop=1, step=25)

    print(t_arr)
    print(s_arr)