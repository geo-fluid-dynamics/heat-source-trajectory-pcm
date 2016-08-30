from scipy.optimize import minimize
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import pandas

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
        self.time = 0.
        self.time_history = self.make_time_history_row()


    def run_step(self):
        self.pde.end_time = self.input.time_step
        self.pde.solve(self)

        def increment_data():
            self.time += self.input.time_step
            self.step += 1
            new_row = self.make_time_history_row()
            print(new_row)
            self.time_history = self.time_history.append(new_row)

        def objective(x):
            gravity_aligned_axis = 1
            return self.body.get_center_of_gravity(x)[gravity_aligned_axis]

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
        bounds = ((0., 0.), (self.state[1] - reference_length, self.state[1] + reference_length), (0., 0.))
        # Verify that the initial guess does not violate any constraints.
        epsilon = 1e-6
        constraint_values = constraints(self.state)
        if any(constraint_values < -epsilon):
            increment_data()
            return
        assert(not any(constraint_values < -epsilon))
        #
        output = minimize(fun=objective, x0=self.state, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
        # Verify that the solution does not violate any constraints.
        # scipy.minimize likes to return "success" even though constraints are violated.
        constraint_values = constraints(output.x)
        assert(not any(constraint_values < -epsilon)) 
        #
        assert(not any(np.isnan(output.x)))
        #
        self.state = output.x
        # @todo: Warn if solution is on boundary.

        #
        increment_data()


    def make_time_history_row(self):
        return pandas.DataFrame({'step': self.step, 'time': self.time,
                                'lateral': self.state[0], 'depth': self.state[1], 'rotation': self.state[2]},
                                index=[self.step])


    def run(self):
        print("Running trajectory \'"+self.input.name+'\'')
        if not os.path.exists(self.input.name):
            os.makedirs(self.input.name)
        print(self.time_history)
        self.pde.n_adaptive_pre_refinement_steps = 0
        while self.step < self.input.step_count:
            self.old_state = self.state
            self.run_step()
            self.plot_frame()
            self.pde.interpolate_old_field = True


    def write_time_history(self):
        self.time_history.to_csv(self.input.name+'_time_history.csv')

    # @todo: plot frames with Paraview

    def plot_frame(self):    
        xi_grid, yi_grid = plots.grid_sample_points(self.pde.data)
        ui = self.pde.interpolator(xi_grid, yi_grid)
        plt.xlabel('x')
        plt.ylabel('y')
        if self.input.plot_xlim:
            plt.xlim(self.input.plot_xlim)
            plt.ylim(self.input.plot_ylim)
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')
        cp = plt.contour(xi_grid, yi_grid, ui.reshape(xi_grid.shape),
                         (0.8*self.environment.temperature,
                         self.environment.material['melting temperature']),
                         colors=('k', 'b'))
        plt.clabel(cp, inline=True, fontsize=10)
        points = body.close_curve(self.body.get_hull_points(self.old_state))
        plt.plot(points[:, 0], points[:, 1], '--y', label='Old State')
        points = body.close_curve(self.body.get_hull_points(self.state))
        plt.plot(points[:, 0], points[:, 1], '-r', label='Current State')
        plt.legend()
        plt.title('Step '+str(self.step))
        plt.savefig(self.input.name+'\\trajectory_frame_'+str(self.step))
        plt.cla()


    def plot_time_history(self):
        fig = plt.figure()
        plt.xlabel('Time [time units]')
        plt.ylabel('Depth [distance units]')
        plt.grid()
        axes = fig.add_subplot(111)
        axes.plot(self.time_history[:,0], self.time_history[:,2], label=self.input.name)
        axes.autoscale_view(True,True,True)


    def test(self):
        self.run()


if __name__ == "__main__":
    trajectory = Trajectory()
    trajectory.test()
