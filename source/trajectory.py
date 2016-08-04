from scipy.interpolate import Rbf
from scipy.optimize import minimize
import numpy as np
import math
import field
import body


def move(old_points, x):
    assert(x.size == 3)  # 2D
    theta = x[2]
    rotation_matrix = np.matrix([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    points = np.matrix(old_points)*rotation_matrix
    points = points + x[:2]
    return points


def step_trajectory(initial_state):
    points = body.get_hull_points()
    data = field.get_data(initial_state) - field.melt_temperature
    interpolant = Rbf(data[:, 0], data[:, 1], data[:, 2], function='multiquadric')
    center_of_gravity = body.get_center_of_gravity()

    def objective(x):
        new_cg = move(center_of_gravity, x)
        return new_cg[0, 1]

    def constraints(x):
        new_points = move(points, x)
        # How can I create an "interpolant" similar to scatteredInterpolant in MATLAB rather than doing this every time?
        values = interpolant(new_points[:, 0], new_points[:, 1])
        return values

    state = minimize(fun=objective, x0=initial_state,
                     constraints={'type': 'ineq', 'fun': constraints},
                     bounds=((None, None), (None, None), (-math.pi/2., math.pi/2.)))
    return state


def migrate():
    initial_state = (0., 0., 0.)
    state = initial_state
    step_count = 2
    print(state)
    for step in range(0, step_count):
        state = step_trajectory(state)
        print(state)


def test():
    migrate()


if __name__ == "__main__":
    test()
