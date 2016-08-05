from scipy import interpolate
from scipy.optimize import minimize
import numpy as np
import math
import field
import body
import plots


def step_trajectory(initial_state, step):
    reference_points = body.get_hull_points()
    initial_points = body.get_hull_points(initial_state)
    data = field.solve_pde(initial_state)
    # Extrapolate constant values, because NaN's break SciPy.optimize.minimize
    interpolator = interpolate.LinearNDInterpolator(data[:, :2], data[:, 2], fill_value=field.temperature)
    center_of_gravity = body.get_center_of_gravity()

    def objective(x):
        new_cg = body.move(center_of_gravity, x)
        return new_cg[0, 1]

    def constraints(x):
        new_points = body.move(reference_points, x)
        values = interpolator(new_points[:, :2])
        return values

    bounds = ((min(data[:, 0]) - min(reference_points[:, 0]), max(data[:, 0]) - max(reference_points[:, 0])),
              (min(data[:, 1]) - min(reference_points[:, 1]), max(data[:, 1]) - max(reference_points[:, 1])),
              (-math.pi/2., math.pi/2.))
    output = minimize(fun=objective, x0=initial_state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
    state = output.x
    plots.plot_frame(interpolator, data, initial_state, state, step+1)
    return state


def migrate(step_count=5):
    initial_state = np.array((0., 0., 0.))
    state = initial_state
    print(state)
    for step in range(0, step_count):
        state = step_trajectory(state, step)
        print(state)


def test():
    migrate()


if __name__ == "__main__":
    test()
