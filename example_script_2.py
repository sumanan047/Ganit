import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

from nietzsche.time_ import Time
from nietzsche.space import Space
from nietzsche.pde import Diffusion
from nietzsche.utils import Dimension

# set space
s = Space()
s.dimension = Dimension.DDD.value  # DD for 2D
sp = s.setup(x_step=60, y_step=60, z_step=60)

# set time
time = Time()
t = time.setup(step=600)

# set diffusion
diff = Diffusion()
diff.set_primal_domain(space_array=sp, time_array=t)
diff.initial_condition(general_value=0.0,
                        specific_value=4.00,
                        x_ilocation=14,
                        x_elocation=26,
                        y_ilocation=10,
                        y_elocation=20,
                        z_ilocation=10,
                        z_elocation=20)
diff.primal_domain = diff.boundary_condition(diff.primal_domain,
                                                constant_value=0.0,
                                                thickness=1)
diff.solve(step_constant=0.03)
diff.export_result()
# animate directly from the function
if diff.primal_domain.ndim == 1 or diff.primal_domain.ndim == 2 or diff.primal_domain.ndim ==3:
    anim = animation.FuncAnimation(plt.figure(),
                                diff.animate,
                                interval=0.5,
                                frames=len(t),
                                repeat=False)
    anim.save(f"{s.dimension}D-heat_equation_solution.gif")
elif diff.primal_domain.ndim == 4: 
    mlab.figure(size=(800, 600))
    for k in range(len(diff.primal_domain)):
        src = mlab.pipeline.scalar_field(diff.primal_domain[k, :, :, :])
        mlab.clf() # clear the figure before plotting the next frame
        vol = mlab.pipeline.volume(src)
        vol.module_manager.scalar_lut_manager.lut.table = vol.module_manager.scalar_lut_manager.lut.table 
        mlab.axes()
        mlab.title(f"Pressure at time = {k*diff.dt:.1f} unit time")
        # mlab.show()
        mlab.savefig(f"frame_{k}.png")
    mlab.close()
    images = [imageio.v2.imread(f"frame_{k}.png") for k in range(len(diff.primal_domain))]
    # create a gif from the images
    imageio.mimsave("3D-heat_equation_solution.gif", images, fps=10)
    # remove the png files
    import os
    for k in range(len(diff.primal_domain)):
        os.remove(f"frame_{k}.png")