#!/usr/bin/python
import trajectory

def test():

    traj = trajectory.Trajectory()
    traj.run()
    #
    traj = trajectory.Trajectory()
    traj.input.name = "turn"
    traj.pde.input.dirichlet_boundary_values[-1] = 0.1
    traj.run()


if __name__ == "__main__":
    test()
