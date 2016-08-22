from scipy import interpolate
from scipy.optimize import minimize
import numpy as np
import math

import input
import pde
import body
import plots

reference_points = body.get_hull_points()
reference_state = np.array((0., 0., 0.))

def step_trajectory(initial_state, step):
    data = pde.solve(step, initial_state)
    interpolator = interpolate.LinearNDInterpolator(data[:, :2], data[:, 2], fill_value=input.field['temperature'])

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
    # @todo: For a case with ten trajectory steps, it was observed that the minimized state was not tipping all
    #        the way against the melt boundary on steps 7 and 9. This is an open issue.
    r = input.body['sphere_radius']
    bounds = ((initial_state[0] - r, initial_state[0] + r),
              (initial_state[1] - r, initial_state[1] + r),
              (initial_state[2] - max_turn_angle, initial_state[2] + max_turn_angle))
    # @todo: Warn if solution is on boundary.
    output = minimize(fun=objective, x0=initial_state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
    state = output.x
    assert(not any(np.isnan(state)))
    plots.plot_frame(interpolator, data, initial_state, state, step+1)
    return state


def migrate(step_count=input.trajectory['step_count']):
    state = reference_state
    for step in range(0, step_count):
        print('Step = '+str(step))
        state = step_trajectory(state, step)


def test():
    migrate()


if __name__ == "__main__":
    test()
