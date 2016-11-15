#!/usr/bin/python
import trajectory
import pde
import matplotlib.pyplot as plt
import pandas


t = trajectory.Trajectory()

t.input.name = 'step_heat'

t.input.step_count = 10
t.input.time_step_size = 1.

t.state.velocity[1] = -0.001

r = 1.e-2
t.body.input.sphere_radius = r

t.pde.input.geometry.dim = 2
t.pde.input.geometry.grid_name = 'hyper_shell'
t.pde.input.geometry.sizes = [r, 2*r]

t.pde.input.use_physical_diffusivity = True

t.pde.input.bc.implementation_types = ['natural', 'strong']
t.pde.input.bc.function_names = ['constant', 'constant']
t.pde.input.bc.function_double_arguments = [2.e-3, -1.]

t.pde.input.iv.function_name = 'constant'
t.pde.input.iv.function_double_arguments = -1.

t.pde.input.refinement.boundaries_to_refine = 0
t.pde.input.refinement.initial_boundary_cycles = 3
t.pde.input.refinement.initial_global_cycles = 2

t.pde.input.time.semi_implicit_theta = 1.
t.pde.input.time.step_size = 0.2

t.pde.input.solver.tolerance = 1.e-8
t.pde.input.solver.normalize_tolerance = False

t.run()

t.input.step_count = 20
t.pde.input.bc.function_double_arguments[0] = 1.2*t.pde.input.bc.function_double_arguments[0]
t.run()

print(t.time_history)
t.write_time_history()
    