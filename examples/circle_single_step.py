#!/usr/bin/python
import trajectory
import pandas
        
t = trajectory.Trajectory()
    
t.name = 'circle_single_step'

r = 1.
t.body.sizes[0] = r

t.max_change = [0., r/2., 0.]

t.pde.geometry.grid_name = 'hyper_shell'
t.pde.geometry.sizes = [r, 2*r]

t.pde.bc.implementation_types = ['natural', 'strong']
t.pde.bc.function_names = ['constant', 'constant']
t.pde.bc.function_double_arguments = [2., -1.]

t.pde.iv.function_name = 'constant'
t.pde.iv.function_double_arguments = -1.

t.pde.refinement.initial_global_cycles = 5

t.pde.time.step_size = 0.2

t.run_step(True, True, True)
