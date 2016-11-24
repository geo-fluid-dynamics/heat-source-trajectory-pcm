#!/usr/bin/python
import trajectory
import pandas

def make_time_history_row(traj):
    return pandas.DataFrame(
        {'step': traj.step, 'time': traj.time,
         'velocity': traj.state_dot.get_position()[1],
         'depth': traj.state.get_position()[1],
         'pde_depth': traj.pde.state.get_position()[1],
         'heat_flux': traj.pde.input.bc.function_double_arguments[0]},
        index=[traj.step])
        
        
t = trajectory.Trajectory()
time_history = make_time_history_row(t)

t.input.name = 'constant_heat'

t.input.time_step_size = 1.

t.state_dot.position[1] = -0.001

r = 1.e-2
t.body.input.sizes = [r]

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

time_history =  make_time_history_row(t)
print(time_history)

print("Running trajectory \'"+t.input.name+'\'')

for step in range(0,3):
    t.run_step()
    time_history = time_history.append(make_time_history_row(t))
    print(time_history)

time_history.to_csv(t.input.name+'/time_history.csv')