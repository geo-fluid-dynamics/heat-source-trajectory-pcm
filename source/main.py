#!/usr/bin/python
import trajectory
import pde
import matplotlib.pyplot as plt
import pandas


def run():
    
    #run_turn()
    run_sphere_cylinder()
    #run_superposed_advection()

    
def run_turn():
    t = setup_sphere_cylinder()
    t.pde.input.bc.implementation_types[9] = 'strong'
    t.pde.input.bc.implementation_types[5] = 'strong'
    t.pde.input.bc.function_double_arguments[9] = 0.5
    t.pde.input.bc.function_double_arguments[5] = 1.
    t.run()
    
    
def run_sphere_cylinder():
    t = setup_sphere_cylinder()
    t.run()
    
    
def setup_sphere_cylinder():
    t = trajectory.Trajectory()
    t.input.name = 'sphere_cylinder_straight_down'
    t.input.time_step_size = 0.05
    t.input.step_count = 10 # @todo: Something is broken after the first step for small time step size
    
    t.body.input.geometry_name = 'sphere-cylinder'
    L = 0.125
    t.body.input.sizes = [L, 0.875]
    t.body.input.reference_length = L
    
    t.pde.input.enable_convection = False
    t.pde.input.geometry.grid_name = 'hemisphere_cylinder_shell'
    t.pde.input.geometry.sizes = [L, 1.25, 1.0, 3.0]
    t.pde.input.bc.implementation_types = [
        'strong', 'natural', 'natural', 'natural', 'strong',
        'natural', 'strong', 'strong', 'strong', 'natural']
    t.pde.input.bc.function_names = [
        'constant', 'constant', 'constant', 'constant', 'constant',
        'constant', 'constant', 'constant', 'constant', 'constant']
    t.pde.input.bc.function_double_arguments = [
        -1., 0., 0., 0., -1., 10., 0.1, 0.1, 0.1, 10.]
    t.pde.input.refinement.initial_global_cycles = 0
    t.pde.input.refinement.boundaries_to_refine = [5, 6, 7, 8, 9]
    t.pde.input.refinement.initial_boundary_cycles = 5
    t.pde.input.time.step_size = 0.005
    t.pde.input.use_physical_diffusivity = False
    
    t.input.plot_xlim = [-1., 1.]
    t.input.plot_ylim = [-1.5, 1.5]
    
    return t
    
    
def run_superposed_advection():

    t = trajectory.Trajectory()
    
    t.input.name = 'superposed_advection'
    
    t.input.step_count = 5
    t.input.time_step_size = 10.
    t.state.velocity = [0., 0.001]
    
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
    t.pde.input.time.step_size = 1.

    t.pde.input.solver.tolerance = 1.e-8
    t.pde.input.solver.normalize_tolerance = False

    t.run()

    print(t.time_history)
    t.write_time_history()


if __name__ == "__main__":
    run()
