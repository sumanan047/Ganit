import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

from time_ import Time
from space import Space
from pde import Diffusion
from utils import Dimension


if __name__ == "__main__":
    # ========= IMPLEMENTATION ========================
    # set space
    s = Space()
    s.dimension = Dimension.D.value  # DD for 2D
    sp = s.setup(x_step=60, y_step=60, z_step=60)

    # set time
    time = Time()
    t = time.setup(step=60)

    # set diffusion
    diff = Diffusion()
    diff.set_primal_domain(space_array=sp, time_array=t)
    diff.initial_condition(general_value=0.0,
                            specific_value=40.00,
                            x_ilocation=44,
                            x_elocation=46,
                            y_ilocation=10,
                            y_elocation=15,
                            z_ilocation=10,
                            z_elocation=15)
    diff.primal_domain = diff.boundary_condition(diff.primal_domain,
                                                    constant_value=0.0,
                                                    thickness=1)
    diff.solve(step_constant=0.03)

    # write the simulation result in a csv
    diff.export_result()

    # animate directly from the function
    anim = animation.FuncAnimation(plt.figure(),
                                    diff.animate,
                                    interval=0.5,
                                    frames=len(t),
                                    repeat=False)
    anim.save(f"{s.dimension}D-heat_equation_solution.gif")
