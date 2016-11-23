from scipy.optimize import minimize
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas
import copy

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
        self.state_dot = state_module.State()
        
        self.old_state = state_module.State()
        
        self.step = 0
        self.time = 0.
        self.time_history = self.make_time_history_row()

        
    def make_time_history_row(self):
        return pandas.DataFrame(
            {'step': self.step, 'time': self.time,
             'velocity': self.state_dot.get_position()[1],
             'depth': self.state.get_position()[1],
             'pde_depth': self.pde.state.get_position()[1],
             'heat_flux': self.pde.input.bc.function_double_arguments[0]},
            index=[self.step])
        
        
    def run_step(self):
        self.pde.state_dot = -1*self.state_dot
        self.pde.input.time.end_time = self.input.time_step_size
        
        self.pde.solve(self) # @todo: Why does PDE need a Trajectory input?
        
        def increment_data():
            self.time += self.input.time_step_size
            self.step += 1
            new_row = self.make_time_history_row()
            print(new_row)
            self.time_history = self.time_history.append(new_row)

            
        def x_to_state(x):
            state = state_module.State()
            position = state.get_position()
            orientation = state.get_orientation()
            
            if x.size == 3:
                position[:2] = x[:2]
                position[2] = 0
                orientation[0] = x[2]
                orientation[1] = 0
                orientation[2] = 0
                
            elif x.size == 6:
                position = x[:3]
                orientation = x[3:]
                
            state.set_position(position)
            state.set_orientation(orientation)
            return state
            
            
        def state_to_x(state, ndof):
            position = state.get_position()
            orientation = state.get_orientation()
            
            if ndof == 3:
                x = np.array([0., 0., 0.])
                x[:2] = position[:2]
                x[2] = orientation[0]
                return x
                
            elif ndof == 6:
                x = np.array([0., 0., 0., 0., 0., 0.])
                x[:3] = position[:]
                x[3:] = orientation[:]
                return x
        
            
        def objective(x):
            gravity_aligned_axis = 1 # @todo: Generalize the gravity vector
            state = x_to_state(x)
            return self.body.get_center_of_gravity(state)[gravity_aligned_axis]
           
           
        def constraints(x):
            state = x_to_state(x)
            return self.pde.interpolator(self.body.get_hull_points(state))

            
        x0 = state_to_x(self.pde.state, 3)
        
        # Verify that the initial guess does not violate any constraints.
        epsilon = 1e-6
        constraint_values = constraints(x0)
        if any(constraint_values < -epsilon):
            increment_data()  # This allows us to animate the trajectory when the body isn't yet moving.
            return

        assert(not any(constraint_values < -epsilon))
        
        # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
        # We must limit x away from the boundary of the domain.
        # Since the domain will be relatively large compared to the body, and movements should be in small increments.
        # it should suffice to bound the movement relative to a reference length.

        reference_length = self.body.input.reference_length
        bounds = (
            (0., 0.), # @todo: Enable lateral motion
            (x0[1] - reference_length, x0[1] + reference_length),
            (0., 0.)) # @todo: Enable rotation
        
        output = minimize(fun=objective, x0=x0, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds)
        
        print(output)
        assert(not any(np.isnan(output.x)))
        
        # Verify that the solution does not violate any constraints.
        # scipy.minimize likes to return "success" even though constraints are violated.
        constraint_values = constraints(output.x)
        assert(not any(constraint_values < -epsilon)) 

        plot_delta_x =  self.state_dot.get_position()[0]*self.input.time_step_size
        self.input.plot_xlim[0] = self.input.plot_xlim[0] + plot_delta_x
        self.input.plot_xlim[1] = self.input.plot_xlim[1] + plot_delta_x
        plot_delta_y = self.state_dot.get_position()[1]*self.input.time_step_size
        self.input.plot_ylim[0] = self.input.plot_ylim[0] + plot_delta_y
        self.input.plot_ylim[1] = self.input.plot_ylim[1] + plot_delta_y
        
        delta_state = x_to_state(output.x) - self.pde.state
        self.state = self.state + delta_state + self.input.time_step_size*self.state_dot
        self.state_dot = self.state_dot + self.input.time_step_size*delta_state
        
        self.pde.state = self.pde.state + delta_state

        increment_data()
        

    def run(self):

        print("Running trajectory \'"+self.input.name+'\'')

        if not os.path.exists(self.input.name):
            os.makedirs(self.input.name)

        print(self.time_history)

        while self.step < self.input.step_count:
            self.old_state = copy.deepcopy(self.state)
            self.run_step()
            file_path = self.input.name+'/trajectory_step'+str(self.step)

            assert(self.pde.state.orientation[0] == 0.) # @todo: Also rotate the frame
            
            self.plot_frame(file_path+'_FixedViewFrame')
                
            self.pde.interpolate_old_field = True

    def write_time_history(self):
        self.time_history.to_csv(self.input.name+'_time_history.csv')

    # @todo: plot frames with ParaView

    def plot_frame(self, file_path):           
        xi_grid, yi_grid = plots.grid_sample_points(self.pde.data)
        delta_y = self.state.get_position()[1] - self.pde.state.get_position()[1]
        ui = self.pde.interpolator(xi_grid, yi_grid - delta_y)
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
