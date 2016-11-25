from scipy.optimize import minimize
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import pandas
import copy

import state
import environment
import pde
import body
import plot


class Trajectory:
    
    def __init__(self):
        self.name = 'default'
        self.time_step_size = 1.
        
        self.body = body.Body()
        self.pde = pde.PDE(self.body)
        self.environment = environment.Environment()
        
        self.state = state.State()
        self.state_dot = state.State()
        
        self.old_state = state.State()
        
        self.step = 0
        self.time = 0.
        
        self.max_change = [1., 1., math.pi/8.]

        
    def run_step(self, display_convergence=False):
 
        if not os.path.exists(self.name):
            os.makedirs(self.name)
        
        self.old_state = copy.deepcopy(self.state)
    
        self.pde.state_dot = -1*self.state_dot
        self.pde.time.end_time = self.time_step_size
        
        # The PDE solver needs to access many members of self; maybe there's a better way to do this without the circular dependency.
        self.pde.solve(self)
        
        def increment_data():
            self.time += self.time_step_size
            self.step += 1
            file_path = self.name+'/trajectory_step'+str(self.step)
            plot.plot_frame(self, file_path)

            
        def x_to_state(x):
            s = state.State()
            position = s.get_position()
            orientation = s.get_orientation()
            
            if x.size == 3:
                position[:2] = x[:2]
                position[2] = 0
                orientation[0] = x[2]
                orientation[1] = 0
                orientation[2] = 0
                
            elif x.size == 6:
                position = x[:3]
                orientation = x[3:]
                
            s.set_position(position)
            s.set_orientation(orientation)
            return s
            
            
        def state_to_x(s, ndof):
            position = s.get_position()
            orientation = s.get_orientation()
            
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
            return self.body.get_center_of_gravity(x_to_state(x))[gravity_aligned_axis]
           
           
        def constraints(x):
            return self.pde.interpolator(self.body.get_hull_points(x_to_state(x)))

            
        x0 = state_to_x(self.pde.state, 3)
        
        # Verify that the initial guess does not violate any constraints.
        epsilon = 1e-6
        constraint_values = constraints(x0)
        if any(constraint_values < -epsilon):
            increment_data()  # This allows us to animate the trajectory when the body isn't yet moving.
            print('The initial state violates the constraints. Skipping minimization')
            return

        assert(not any(constraint_values < -epsilon))
        
        # Because we're numerically approximating the derivative, SLSQP breaks at the outer boundary.
        # We must limit x away from the boundary of the domain.
        # Since the domain will be relatively large compared to the body, and movements should be in small increments.
        # it should suffice to bound the movement relative to a reference length.

        reference_length = self.body.reference_length
        bounds = (
            (x0[0] - self.max_change[0], x0[0] + self.max_change[0]),
            (x0[1] - self.max_change[1], x0[1] + self.max_change[1]),
            (x0[2] - self.max_change[2], x0[2] + self.max_change[2]))
        
        print('Minimizing objective')
        
        output = minimize(fun=objective, x0=x0, constraints={'type': 'ineq', 'fun': constraints}, bounds=bounds, options={'disp': display_convergence})
        
        print(output)
        assert(not any(np.isnan(output.x)))
        
        # Verify that the solution does not violate any constraints.
        # scipy.minimize likes to return "success" even though constraints are violated.
        constraint_values = constraints(output.x)
        assert(not any(constraint_values < -epsilon)) 
        
        new_pde_state = x_to_state(output.x) 
        delta_state = new_pde_state - self.pde.state
        self.pde.state = new_pde_state
        
        self.state = self.state + delta_state + self.time_step_size*self.state_dot
        self.state_dot = self.state_dot + (1./self.time_step_size)*delta_state

        increment_data()
            
        self.pde.interpolate_old_field = True
        

    def run_steps(self, step_count):
        for step in range(0, step_count):            
            self.run_step()


if __name__ == "__main__":
    traj= Trajectory()
    traj.run_steps(2)
