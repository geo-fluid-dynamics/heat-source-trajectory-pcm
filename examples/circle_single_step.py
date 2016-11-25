#!/usr/bin/python
import trajectory
import pandas
        
t = trajectory.Trajectory()
    
t.name = 'circle_single_step'

t.time_step_size = 1.

r = 1.e-2
t.body.sizes[0] = r

t.max_change = [0., r/2., 0.]

t.pde.geometry.dim = 2
t.pde.geometry.grid_name = 'hyper_shell'
t.pde.geometry.sizes = [r, 2*r]

t.pde.use_physical_diffusivity = True

t.pde.bc.implementation_types = ['natural', 'strong']
t.pde.bc.function_names = ['constant', 'constant']
t.pde.bc.function_double_arguments = [2.e-3, -1.]

t.pde.iv.function_name = 'constant'
t.pde.iv.function_double_arguments = -1.

t.pde.refinement.boundaries_to_refine = 0
t.pde.refinement.initial_boundary_cycles = 3
t.pde.refinement.initial_global_cycles = 2

t.pde.time.semi_implicit_theta = 1.
t.pde.time.step_size = 0.2

t.pde.solver.tolerance = 1.e-8
t.pde.solver.normalize_tolerance = False

t.run_step(True, True, True)
