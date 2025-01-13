import numpy as np
import matplotlib.pyplot as plt

from nietzsche.utils import Dimension
from nietzsche.time_ import Time
from nietzsche.space import Space
from nietzsche.vibration import Vibration
from nietzsche.initial_condition import InitialConditions

# set time
t = Time(start = 0.0, step = 100, dt = 0.1)

# set space
s = Space(dimension=Dimension.DD.value, x_start=0, x_stop=1, x_step=25)

# set vibration
v = Vibration(time=t, space=s)

# set initial conditions
def quad_func(x):
    return 34*np.sin(x)*np.cos(x)

ic = InitialConditions(domain=np.linspace(0, 1, 10), mode="function", value=10, funcion=quad_func)
ic.set()


# plot to debug
plt.plot(ic.domain,ic.ic_arr)
plt.show()