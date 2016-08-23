#!/usr/bin/python
import trajectory


def run():
    run_default()
    run_turn()
    run_s_turn()
    run_smooth_s_turn()
    #run_turn_with_ramped_nose_bc()


def run_default():
    traj = trajectory.Trajectory()
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


if __name__ == "__main__":
    run()
