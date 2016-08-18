from scipy import interpolate
from scipy.optimize import minimize
import numpy as np
import math
import field
import body
import plots
reference_points = body.get_hull_points()
reference_state = np.array((0., 0., 0.))

def step_trajectory(initial_state, step):
    data = field.solve_pde(initial_state)
    interpolator = interpolate.LinearNDInterpolator(data[:, :2], data[:, 2], fill_value=field.temperature)

    def objective(x):
        return body.get_center_of_gravity(x)[1]

    def constraints(x):
        return interpolator(body.get_hull_points(x))

    initial_hull_points = body.get_hull_points(initial_state)
    # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
    # We must limit x away from the boundary of the domain.
    # Since the domain will be relatively large compared to the body, and movements should be in small increments.
    # it should suffice to bound the movement relative to the size of the spherical nose.
    max_turn_angle = math.pi/16.
    bounds = ((initial_state[0] - body.sphere_radius, initial_state[0] + body.sphere_radius),
              (initial_state[1] - body.sphere_radius, initial_state[1] + body.sphere_radius),
              (-max_turn_angle, max_turn_angle))
    # @todo: Warn if solution is on boundary.
    output = minimize(fun=objective, x0=initial_state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
    state = output.x
    assert(not any(np.isnan(state)))
    plots.plot_frame(interpolator, data, initial_state, state, step+1)
    return state


def migrate(step_count=3):
    state = reference_state
    for step in range(0, step_count):
        print('Step = '+str(step))
        state = step_trajectory(state, step)


def test():
    migrate()


if __name__ == "__main__":
    test()
