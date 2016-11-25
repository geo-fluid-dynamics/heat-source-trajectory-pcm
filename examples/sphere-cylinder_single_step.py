#!/usr/bin/python
import trajectory
import pandas

t = trajectory.Trajectory()
    
t.name = 'sphere-cylinder_single_step'

t.time_step_size = 1.

t.body.geometry_name = 'sphere-cylinder'
r = 0.1
L = 1
t.body.sizes = [r, L]

t.pde.geometry.dim = 2
t.pde.geometry.grid_name = 'hemisphere_cylinder_shell'
t.pde.geometry.sizes = [r, r + 3*r, L, L + 3*r]

t.pde.bc.implementation_types = ['strong', 'strong', 'strong', 'strong', 'strong',
    'strong', 'strong', 'strong', 'strong', 'strong']
t.pde.bc.function_names = ['constant', 'constant', 'constant', 'constant', 'constant',
    'constant', 'constant', 'constant', 'constant', 'constant']
t.pde.bc.function_double_arguments = [-1, -1, -1, -1, -1,
    1, 0.1, 0.1, 0.1, 0.2]

t.pde.iv.function_name = 'constant'
t.pde.iv.function_double_arguments = -1.

t.pde.refinement.initial_global_cycles = 5

t.pde.time.semi_implicit_theta = 1.
t.pde.time.step_size = 0.2

t.run_step(True, True, True)
