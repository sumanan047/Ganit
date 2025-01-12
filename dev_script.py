from nietzsche.utils import Dimension
from nietzsche.time_ import Time
from nietzsche.space import Space
from nietzsche.vib_ode import Vibration

# set time
t = Time(start = 0.0, step = 100, dt = 0.1)

# set space
s = Space(dimension=Dimension.DD.value, x_start=0, x_stop=1, x_step=25)

# set vibration
v = Vibration(time=t, space=s)

print(v.primal_domain.shape)