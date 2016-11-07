from scipy.optimize import minimize
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas

import inputs
import state as state_module
import pde
import body
import plots


class Trajectory:
    def __init__(self):
        self.input = inputs.TrajectoryInputs()
        self.body = body.Body()
        self.pde = pde.PDE(self.body)
        self.environment = inputs.EnvironmentInputs()
        self.state = state_module.State()
        self.old_state = state_module.State()
        self.step = 0
        self.time = 0.
        self.time_history = self.make_time_history_row()

    def run_step(self):
        self.pde.input.time.end_time = self.input.time_step_size
        self.pde.solve(self)

        def increment_data():
            self.time += self.input.time_step_size
            self.step += 1
            new_row = self.make_time_history_row()
            print(new_row)
            self.time_history = self.time_history.append(new_row)

        def x_to_new_state(x):
            state = state_module.State()
            state.set_position(self.pde.state.get_position())
            state.orientation[0] = self.pde.state.orientation[0]
            
            position = state.get_position()
            position[0] = position[0] + x[0]
            position[1] = position[1] + x[1]
            
            state.set_position(position)
            
            state.orientation[0] = x[2]
            
            return state
        
            
        def objective(x):
            gravity_aligned_axis = 1
            state = x_to_new_state(x)
            return self.body.get_center_of_gravity(state)[gravity_aligned_axis]
                
        def constraints(x):
            state = x_to_new_state(x)
            return self.pde.interpolator(self.body.get_hull_points(state))
            

        # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
        # We must limit x away from the boundary of the domain.
        # Since the domain will be relatively large compared to the body, and movements should be in small increments.
        # it should suffice to bound the movement relative to a reference length.

        reference_length = self.body.input.reference_length
        bounds = (
            (0., 0.),
            (-reference_length, reference_length),
            (0., 0.))

        # Verify that the initial guess does not violate any constraints.
        epsilon = 1e-6
        x = np.array((0., 0., 0.))
        constraint_values = constraints(x)
        if any(constraint_values < -epsilon):
            increment_data()  # This allows us to animate the trajectory when the body isn't yet moving.
            return

        assert(not any(constraint_values < -epsilon))
        #

        x0 = np.array([0., 0., 0.])
        x0[:2] = self.pde.state.get_position()[:2]
        x0[2] = self.pde.state.orientation[0]
        output = minimize(fun=objective, x0=x0, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
        # Verify that the solution does not violate any constraints.
        # scipy.minimize likes to return "success" even though constraints are violated.
        constraint_values = constraints(output.x)
        assert(not any(constraint_values < -epsilon)) 
        
        assert(not any(np.isnan(output.x)))
        
        print(output)
        
        position_update = np.empty_like(self.state.get_position())
        position_update[:2] = output.x[:2]
        position_update[2] = 0.
        
        self.pde.state.set_position(self.pde.state.get_position() + position_update)
        
        orientation_update = np.empty_like(self.state.orientation)
        orientation_update[0] = output.x[2]
        orientation_update[1] = 0.
        orientation_update[2] = 0.
        self.pde.state.orientation[0] = self.pde.state.orientation[0] + orientation_update[0]
        
        position = np.empty_like(self.state.position)
        position[:2] = self.state.get_position()[:2] + position_update[:2]
        position[2] = 0.
        position = position + self.state.velocity*self.input.time_step_size
        self.state.set_position(position)
        
        self.state.orientation = self.state.orientation + orientation_update

        # @todo: Warn if solution is on boundary.

        #
        increment_data()

    def make_time_history_row(self):
        return pandas.DataFrame(
            {'step': self.step, 'time': self.time,
             'lateral': self.state.get_position()[0],
             'depth': self.state.get_position()[1],
             'rotation': self.state.orientation[0],
             'pde_lateral': self.pde.state.get_position()[0],
             'pde_depth': self.pde.state.get_position()[1]},
            index=[self.step])

    def run(self):

        print("Running trajectory \'"+self.input.name+'\'')

        if not os.path.exists(self.input.name):
            os.makedirs(self.input.name)

        print(self.time_history)

        while self.step < self.input.step_count:
            self.old_state.set_position(self.state.get_position())
            self.old_state.orientation[0] = self.state.orientation[0]
            self.run_step()
            file_path = self.input.name+'/trajectory_step'+str(self.step)
            self.plot_frame(file_path+'_MovingViewFrame')

            print('pde.data[:, 1] = ', self.pde.data[:, 1])
            if self.input.plot_fixed_reference_frame:
                print('Plotting from view of fixed reference frame')
                assert(self.pde.state.orientation[0] == 0.) # @todo: Also rotate the frame
                delta_x = self.state.get_position()[0] - self.pde.state.get_position()[0]
                self.pde.data[:, 0] = self.pde.data[:, 0] + delta_x
                delta_y = self.state.get_position()[1] - self.pde.state.get_position()[1]
                print('delta_y = ', delta_y)
                self.pde.data[:, 1] = self.pde.data[:, 1] + delta_y
                print('pde.data[:, 1] = ', self.pde.data[:, 1])
                self.plot_frame(file_path+'_FixedViewFrame')
                
            self.pde.interpolate_old_field = True

    def write_time_history(self):
        self.time_history.to_csv(self.input.name+'_time_history.csv')

    # @todo: plot frames with ParaView

    def plot_frame(self, file_path):           
        xi_grid, yi_grid = plots.grid_sample_points(self.pde.data)
        print('yi_grid = ', yi_grid)
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
        plt.savefig(file_path)
        plt.cla()

    def plot_time_history(self):
        fig = plt.figure()
        plt.xlabel('Time [time units]')
        plt.ylabel('Depth [distance units]')
        plt.grid()
        axes = fig.add_subplot(111)
        axes.plot(self.time_history[:, 0], self.time_history[:, 2], label=self.input.name)
        axes.autoscale_view(True, True, True)

    def test(self):
        self.run()


if __name__ == "__main__":
    trajectory = Trajectory()
    trajectory.test()
