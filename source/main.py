#!/usr/bin/python
import trajectory
import pde
import matplotlib.pyplot as plt
import pandas

def run():
    run_quick()
    #outer_boundary_offset_sensitivity_study()
    #spatial_grid_convergence_study()
    #traj_time_convergence_study()
    #traj_space_convergence_study()
    #pde_time_convergence_study()
    #time_convergence_study()
    #run_default()
    #run_with_neumann_inner_bc()
    #run_with_dirichlet_outer_bc()
    #run_turn()
    #run_s_turn()
    #run_smooth_s_turn()
    #run_turn_with_ramped_nose_bc()
    #run_s_turn_with_narrow_body()


def run_quick():
    end_time = 0.1
    traj_steps = 2
    pde_steps = 4
    #
    traj = trajectory.Trajectory()
    traj.input.name = 'quick'
    traj.input.time_step = end_time/traj_steps
    traj.pde.input.time_step = traj.input.time_step/pde_steps
    traj.pde.input.initial_boundary_refinement = 3
    #
    traj.run()
    print(traj.time_history)
    traj.write_time_history()


def traj_space_convergence_study():
    trajectory_end_time = 0.1
    boundary_refinement_levels = [2, 3, 4, 5, 6]
    total_pde_time_step_count = 32
    pde_time_step_size = trajectory_end_time/total_pde_time_step_count
    # @todo: Try keeping the PDE time step size constant instead.
    trajectory_time_step_counts = [8]
    theta = 1.0
    print('Running '+str(len(boundary_refinement_levels))+' trajectories.')
    for i, boundary_refinement_level in enumerate(boundary_refinement_levels):
        traj = trajectory.Trajectory()
        traj.input.name = 'traj_space_conv_ref'+str(boundary_refinement_level)
        traj.input.step_count = trajectory_time_step_count
        traj.input.time_step = trajectory_end_time/trajectory_time_step_count
        traj.pde.input.initial_boundary_refinement = boundary_refinement_level
        traj.pde.input.time_step = pde_time_step_size
        traj.pde.input.semi_implicit_theta = theta
        traj.run()
        new_rows = traj.time_history
        new_rows['trajectory_time_step_count'] = trajectory_time_step_count
        new_rows['total_pde_time_step_count'] = total_pde_time_step_count
        new_rows['pde_time_step_size'] = pde_time_step_size
        new_rows['boundary_refinement_level'] = boundary_refinement_level
        new_rows['theta'] = theta
        if i == 0:
            table = new_rows
        else:
            table = table.append(new_rows)
        table.to_csv('traj_space_convergence_study_table.csv')
  
    
def outer_boundary_offset_sensitivity_study():
    trajectory_time_step_count = 4
    trajectory_end_time = 0.1
    pde_time_step_count = 32
    outer_boundary_radii = [2, 3, 5]
    boundary_refinement_levels = [3, 4, 5]
    theta = 1.0
    print('Running '+str(len(outer_boundary_radii))+' trajectories.')
    for i, outer_boundary_radius in enumerate(outer_boundary_radii):
        traj = trajectory.Trajectory()
        traj.input.name = 'outer_radius_'+str(outer_boundary_radius)
        traj.input.step_count = trajectory_time_step_count
        traj.input.time_step = trajectory_end_time/trajectory_time_step_count
        traj.pde.input.initial_boundary_refinement = boundary_refinement_levels[i]
        traj.pde.input.time_step = traj.input.time_step/pde_time_step_count
        traj.pde.input.semi_implicit_theta = theta
        traj.pde.input.sizes[1] = outer_boundary_radius
        traj.run()
        new_rows = traj.time_history
        new_rows['trajectory_time_step_count'] = trajectory_time_step_count
        new_rows['pde_time_step_count'] = pde_time_step_count
        new_rows['boundary_refinement_level'] = boundary_refinement_levels[i]
        new_rows['outer_boundary_radius'] = outer_boundary_radius
        new_rows['theta'] = theta
        if i == 0:
            table = new_rows
        else:
            table = table.append(new_rows)
        table.to_csv('outer_boundary_radius_sensitivity_study.csv')

    
def spatial_grid_convergence_study():
    boundary_refinement_levels = [0, 1, 2, 3, 4, 5, 6]
    end_time = 0.10
    step_count = 1
    for i, level in enumerate(boundary_refinement_levels):
        traj = trajectory.Trajectory()
        traj.input.name = 'single_step_gcs_ns'+str(level)
        traj.pde.input.initial_boundary_refinement = level
        traj.input.step_count = step_count
        traj.input.time_step = end_time/step_count
        traj.pde.input.time_step = traj.input.time_step/10
        traj.run()
        new_rows = traj.time_history
        new_rows['step_count'] = step_count
        new_rows['boundary_refinement_level'] = level
        if i == 0:
            table = new_rows
        else:
            table = table.append(new_rows)
        table.to_csv('single_step_spatial_grid_convergence_study_table.csv')
        

def pde_time_convergence_study():
    trajectory_end_time = 0.1
    boundary_refinement_level = 3
    trajectory_time_step_count = 1
    pde_time_step_counts = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    theta = 1.0
    print('Running '+str(len(pde_time_step_counts))+' trajectories.')
    for i, pde_time_step_count in enumerate(pde_time_step_counts):
        traj = trajectory.Trajectory()
        traj.input.name = 'single_step_pde_tcs_ns'+str(boundary_refinement_level)+'_ntt'+str(trajectory_time_step_count)+'_npt'+str(pde_time_step_count)
        traj.input.step_count = trajectory_time_step_count
        traj.input.time_step = trajectory_end_time/trajectory_time_step_count
        traj.pde.input.initial_boundary_refinement = boundary_refinement_level
        traj.pde.input.time_step = traj.input.time_step/pde_time_step_count
        traj.pde.input.semi_implicit_theta = theta
        traj.run()
        new_rows = traj.time_history
        new_rows['trajectory_time_step_count'] = trajectory_time_step_count
        new_rows['boundary_refinement_level'] = boundary_refinement_level
        new_rows['pde_time_step_count'] = pde_time_step_count
        if i == 0:
            table = new_rows
        else:
            table = table.append(new_rows)
        table.to_csv('single_step_pde_time_convergence_study_table.csv')

        
def traj_time_convergence_study():
    trajectory_end_time = 0.1
    boundary_refinement_level = 3
    total_pde_time_step_count = 32
    pde_time_step_size = trajectory_end_time/total_pde_time_step_count
    # @todo: Try keeping the PDE time step size constant instead.
    trajectory_time_step_counts = [1, 2, 4, 8, 16]
    theta = 1.0
    print('Running '+str(len(trajectory_time_step_counts))+' trajectories.')
    for i, trajectory_time_step_count in enumerate(trajectory_time_step_counts):
        traj = trajectory.Trajectory()
        traj.input.name = 'traj_tcs_ntt'+str(trajectory_time_step_count)
        traj.input.step_count = trajectory_time_step_count
        traj.input.time_step = trajectory_end_time/trajectory_time_step_count
        traj.pde.input.initial_boundary_refinement = boundary_refinement_level
        #traj.pde.input.time_step = traj.input.time_step/pde_time_step_count
        traj.pde.input.time_step = pde_time_step_size
        traj.pde.input.semi_implicit_theta = theta
        traj.run()
        new_rows = traj.time_history
        new_rows['trajectory_time_step_count'] = trajectory_time_step_count
        new_rows['total_pde_time_step_count'] = total_pde_time_step_count
        new_rows['pde_time_step_size'] = pde_time_step_size
        new_rows['boundary_refinement_level'] = boundary_refinement_level
        new_rows['theta'] = theta
        if i == 0:
            table = new_rows
        else:
            table = table.append(new_rows)
        table.to_csv('traj_time_convergence_study_table_constant_pde_timestep.csv')


def run_default():
    traj = trajectory.Trajectory()
    traj.run()
    print(traj.time_history)
    traj.write_time_history()


def run_with_neumann_inner_bc():
    traj = trajectory.Trajectory()
    traj.input.name = "neumann_inner_bc"
    cold = traj.pde.input.cold
    warm = traj.pde.input.warm
    hot = traj.pde.input.hot
    traj.pde.input.dirichlet_boundary_ids = [0, 1, 2, 3, 4]
    traj.pde.input.dirichlet_boundary_values = [cold, cold, cold, cold, cold]
    traj.pde.input.dirichlet_ramp_boundary_ids = []
    traj.pde.input.neumann_boundary_ids = [5, 6, 7, 8, 9]
    traj.pde.input.neumann_boundary_values = [10., 5., 5., 5., 10.]
    neumann_boundary_ids = []
    traj.input.step_count = 10
    end_time = 0.03
    time_step = 0.005
    traj.run()


def run_with_dirichlet_outer_bc():
    traj = trajectory.Trajectory()
    traj.input.name = "dirichlet_outer_bc"
    cold = traj.pde.input.cold
    warm = traj.pde.input.warm
    hot = traj.pde.input.hot
    traj.pde.input.dirichlet_boundary_ids = [0, 1, 2, 3, 4, 5, 7, 9]
    traj.pde.input.dirichlet_boundary_values = [cold, cold, cold, cold, cold, hot, warm, hot]
    traj.pde.input.neumann_boundary_ids = []
    traj.input.step_count = 5
    traj.run()


def run_turn():
    traj = trajectory.Trajectory()
    traj.input.name = "turn"
    traj.pde.input.dirichlet_ramp_start_values[1] = traj.pde.input.warm # Make this boundary constant
    traj.pde.input.dirichlet_boundary_values[-1] = traj.pde.input.warm # Cool down this boundary to force a turn
    traj.run()


def run_s_turn():
    traj = trajectory.Trajectory()
    traj.input.name = "s_turn"
    warm = traj.pde.input.warm
    hot = traj.pde.input.hot
    #
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm # Cool down this boundary to force a turn
    traj.run()
    # Stop turning
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 2
    traj.run()
    # Reverse the nose temperatures to turn the other way.
    traj.pde.input.dirichlet_ramp_start_values[1] = hot
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = hot
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 3
    traj.run()


def run_smooth_s_turn():
    traj = trajectory.Trajectory()
    traj.input.name = "smooth_s_turn"
    warm = traj.pde.input.warm
    hot = traj.pde.input.hot
    #
    traj.pde.input.end_time = 0.004
    traj.pde.input.time_step = 0.002
    #
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm # Cool down this boundary to force a turn
    traj.input.step_count = 10
    traj.run()
    # Stop turning
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 2
    traj.run()
    # Reverse the nose temperatures to turn the other way.
    traj.pde.input.dirichlet_ramp_start_values[1] = hot
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = hot
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 10
    traj.run()


def run_turn_with_ramped_nose_bc():
    traj = trajectory.Trajectory()
    traj.input.name = "turn_with_ramped_nose_bc"
    hot = 1.
    warm = 0.1
    R = traj.body.input.sphere_radius
    L = traj.body.input.cylinder_length
    #
    traj.pde.input.dirichlet_boundary_ids = [5, 7, 8]
    traj.pde.input.dirichlet_boundary_values = [hot, warm, warm]
    traj.pde.input.dirichlet_ramp_boundary_ids = [6, 9]
    # @todo: Generalize handling of Dirichlet ramp boundaries
    #        New idea: Ramp every boundary; just set both ends of ramp to same value for constant boundaries
    traj.pde.input.dirichlet_ramp_start_points = [R,  0,
                                                  0, -R]
    traj.pde.input.dirichlet_ramp_end_points = [R, L,
                                               -R, 0]
    traj.pde.input.dirichlet_ramp_start_values = [hot, hot]
    traj.pde.input.dirichlet_ramp_end_values = [warm, warm]
    traj.run()


def run_s_turn_with_narrow_body():
    traj = trajectory.Trajectory()
    traj.input.name = "s_turn_with_narrow_body"
    traj.body.input.sphere_radius = 0.1
    traj.pde = pde.PDE(traj.body)
    warm = traj.pde.input.warm
    hot = traj.pde.input.hot
    #
    traj.body.input.reference_length = traj.body.input.sphere_radius
    traj.pde.input.sizes[1] = 8*traj.body.input.sphere_radius
    traj.pde.input.end_time *= 2
    #
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm # Cool down this boundary to force a turn
    traj.run()
    # Stop turning
    traj.pde.input.dirichlet_ramp_start_values[1] = warm
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = warm
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 1
    traj.run()
    # Reverse the nose temperatures to turn the other way.
    traj.pde.input.dirichlet_ramp_start_values[1] = hot
    traj.pde.input.dirichlet_ramp_start_values[0] = warm
    traj.pde.input.dirichlet_boundary_values[-1] = hot
    traj.pde.input.dirichlet_boundary_values[0] = warm
    traj.input.step_count += 3
    traj.run()


if __name__ == "__main__":
    run()
