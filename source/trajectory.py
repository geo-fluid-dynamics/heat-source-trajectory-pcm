from scipy.optimize import minimize
import numpy as np
import math
import os

import inputs
import pde
import body
import plots

class Trajectory:

    def __init__(self):
        self.input = inputs.TrajectoryInputs()
        self.body = body.Body()
        self.pde = pde.PDE(self.body)
        self.environment = inputs.EnvironmentInputs()
        self.reference_state = np.array((0., 0., 0.))
        self.state = self.reference_state
        self.old_state = self.state
        self.step = 0


    def run_step(self):
        self.pde.solve(self)

        def objective(x):
            return self.body.get_center_of_gravity(x)[1]

        def constraints(x):
            return self.pde.interpolator(self.body.get_hull_points(x))

        initial_hull_points = self.body.get_hull_points(self.state)
        # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
        # We must limit x away from the boundary of the domain.
        # Since the domain will be relatively large compared to the body, and movements should be in small increments.
        # it should suffice to bound the movement relative to the size of the spherical nose.
        max_turn_angle = math.pi/16.
        # @todo: For a case with ten trajectory steps, it was observed that the minimized state was not tipping all
        #        the way against the melt boundary on steps 7 and 9. This is an open issue.
        reference_length = self.body.input.reference_length
        bounds = ((self.state[0] - reference_length, self.state[0] + reference_length),
                  (self.state[1] - reference_length, self.state[1] + reference_length),
                  (self.state[2] - max_turn_angle, self.state[2] + max_turn_angle))
        # @todo: Warn if solution is on boundary.
        output = minimize(fun=objective, x0=self.state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
        self.state = output.x
        assert(not any(np.isnan(self.state)))
        self.step += 1


    def run(self):
        print("Running trajectory \'"+self.input.name+'\'')
        if not os.path.exists(self.input.name):
            os.makedirs(self.input.name)
        while self.step < self.input.step_count:
            print('Step = '+str(self.step))
            self.old_state = self.state
            self.run_step()
            plots.plot_trajectory_frame(self)
            self.pde.interpolate_old_field = True
        with pde.cd(self.pde.input.working_dir):
            os.remove(self.pde.default_parameter_file_name)

    def test(self):
        self.run()


if __name__ == "__main__":
    trajectory = Trajectory()
    trajectory.test()
