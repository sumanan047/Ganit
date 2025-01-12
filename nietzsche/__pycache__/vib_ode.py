# import statements

import numpy as np
import matplotlib.pyplot as plt

# solve 1-D vibration


def space(x_start=0,
          x_stop=1,
          x_step=25,
          y_start=0,
          y_stop=1,
          y_step=25,
          z_start=0,
          z_stop=1,
          z_step=25, mode="3D"):
    x = np.linspace(x_start, x_stop, x_step)
    y = np.linspace(y_start, y_stop, y_step)
    z = np.linspace(z_start, z_stop, z_step)
    if mode == "3D":
        return x, y, z
    elif mode == "2D":
        return x, y
    else:
        return x


def primary_symmetric_field(step, mode="1D"):
    x = np.zeros(step+1)
    y = np.zeros(step+1)
    z = np.zeros(step+1)
    if mode == "3D":
        return x, y, z
    elif mode == "2D":
        return x, y
    elif mode == "1D":
        return x
    else:
        raise ValueError('Please set the mode for the field')


def time(start=0.0, step=100, dt=0.1):
    return np.linspace(start, dt*step, step+1)


def solver(I, w, step, dt):
    u = primary_symmetric_field(step=step)
    u[0] = I
    u[1] = u[0] - 0.5*np.power(dt, 2)*np.power(w, 2)*u[0]
    t = time(start=0.0, step=step, dt=dt)
    for n in range(1, step):
        u[n+1] = 2*u[n] - u[n-1] - np.power(dt, 2)*np.power(w, 2)*u[n]
    return u, t


def actual_sol(t, I, w):
    return I*np.cos(w*t)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--I', type=float, default=1.0)
    parser.add_argument('--w', type=float, default=2*np.pi)
    parser.add_argument('--step', type=int, default=100)
    parser.add_argument('--dt', type=float, default=0.05)
    a = parser.parse_args()
    I, w, step, dt = a.I, a.w, a.step, a.dt
    u, t = solver(I=I, w=w, step=step, dt=dt)
    u_sol = actual_sol(t, I, w)
    plt.plot(t, u, "r--")
    plt.plot(t, u_sol, "b--")
    plt.legend(["Numerical Solution", "Actual Solution"], loc='upper left')
    plt.show()
