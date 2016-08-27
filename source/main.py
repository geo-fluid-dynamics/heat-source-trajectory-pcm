#!/usr/bin/python
import trajectory
import pde


def run():
    run_default()
    #run_with_neumann_inner_bc()
    #run_with_dirichlet_outer_bc()
    #run_turn()
    #run_s_turn()
    #run_smooth_s_turn()
    #run_turn_with_ramped_nose_bc()
    #run_s_turn_with_narrow_body()
    

def run_default():
    traj = trajectory.Trajectory()
    traj.run()


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
