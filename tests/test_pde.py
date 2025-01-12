import pytest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from nietzsche.pde import Diffusion
from nietzsche.space import Space
from nietzsche.time_ import Time
from nietzsche.utils import Dimension

class TestDiffusionHeatmap:

    def setup_method(self):
        self.diffusion = Diffusion()
        self.diffusion.dt = 0.1

    def test_diffusion_heatmap_2d(self):
        self.diffusion.primal_domain = np.random.rand(100, 50)
        k = 10
        pk = self.diffusion.primal_domain[k]
        plt = self.diffusion.diffusion_heatmap(pk, k)
        assert plt.gca().get_title() == f"Pressure at time = {k*self.diffusion.dt:.1f} unit time"
        assert plt.gca().get_xlabel() == "Easting"
        assert plt.gca().get_ylabel() == "Northing"

    def test_diffusion_heatmap_3d(self):
        self.diffusion.primal_domain = np.random.rand(100, 50, 50)
        k = 10
        pk = self.diffusion.primal_domain[k]
        plt = self.diffusion.diffusion_heatmap(pk, k)
        assert plt.gca().get_title() == f"Pressure at time = {k*self.diffusion.dt:.1f} unit time"
        assert plt.gca().get_xlabel() == "Easting"
        assert plt.gca().get_ylabel() == "Northing"

    def test_diffusion_heatmap_invalid_domain(self):
        self.diffusion.primal_domain = None
        k = 10
        with pytest.raises(ValueError, match="This is not Good man"):
            self.diffusion.diffusion_heatmap(None, k)

    def test_full_run(self):
        # ========= IMPLEMENTATION ========================
        # set space
        s = Space()
        s.dimension = Dimension.DD.value  # DD for 2D
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
        if s.dimension == 1:
            diff.export_result()
        elif s.dimension == 2:
            pass
        elif s.dimension == 3:
            pass

        # animate directly from the function
        anim = animation.FuncAnimation(plt.figure(),
                                        diff.animate,
                                        interval=0.5,
                                        frames=len(t),
                                        repeat=False)
        # anim.save(f"{s.dimension}D-heat_equation_solution.gif")