from scipy import interpolate
from scipy.optimize import minimize
import numpy as np
import math
import field
import body
import plots
reference_points = body.get_hull_points()


def step_trajectory(initial_state, step):
    data = field.solve_pde(initial_state)
    interpolator = interpolate.LinearNDInterpolator(data[:, :2], data[:, 2], fill_value=field.temperature)
    plots.plot_interpolator_and_data(interpolator, data)

    def objective(x):
        return body.get_center_of_gravity(x)[1]

    def constraints(x):
        return interpolator(body.get_hull_points(x))

    margin = 1.1  # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
    bounds = (((min(data[:, 0]) - min(reference_points[:, 0]))/margin, max(data[:, 0]) - max(reference_points[:, 0])),
              ((min(data[:, 1]) - min(reference_points[:, 1]))/margin, max(data[:, 1]) - max(reference_points[:, 1])),
              (-math.pi/2., math.pi/2.))
    output = minimize(fun=objective, x0=initial_state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
    state = output.x
    plots.plot_frame(interpolator, data, initial_state, state, step+1)
    return state


def migrate(step_count=1):
    initial_state = np.array((0., 0., 0.))
    state = initial_state
    for step in range(0, step_count):
        print('Step = '+str(step))
        state = step_trajectory(state, step)


def test():
    migrate()


if __name__ == "__main__":
    test()
