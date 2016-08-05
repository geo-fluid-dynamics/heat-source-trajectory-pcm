import invdisttree
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
    interpolant = invdisttree.Invdisttree(data[:, :2], data[:, 2])  # Meshless interpolation
    # @todo: Try probing the solution directly with VTK instead.
    center_of_gravity = body.get_center_of_gravity()

    def objective(x):
        new_cg = move(center_of_gravity, x)
        return new_cg[0, 1]

    def constraints(x):
        new_points = move(points, x)
        # How can I create an "interpolant" similar to scatteredInterpolant in MATLAB rather than doing this every time?
        values = interpolant(new_points[:, :2])
        return values

    state = minimize(fun=objective, x0=initial_state,
                     constraints={'type': 'ineq', 'fun': constraints},
                     bounds=((min(data[:, 0]) - min(points[:, 0]), max(data[:, 0]) - max(points[:, 0])),
                             (min(data[:, 1]) - min(points[:, 1]), max(data[:, 1]) - max(points[:, 1])),
                             (-math.pi/2., math.pi/2.)))
    return state.x


def migrate():
    initial_state = np.array((0., 0., 0.))
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
