class TrajectoryInputs:
    name = 'default'
    step_count = 3


class BodyInputs:
    sphere_radius = 0.25
    cylinder_length = 1.0
    geometry_name = 'hemisphere_cylinder_shell'
    sizes = [sphere_radius, 2*sphere_radius, cylinder_length, 2*cylinder_length]
    arc_point_count = 11
    line_point_count = 11
    reference_length = sphere_radius


class EnvironmentInputs:
    temperature = -1.
    material = {'name': 'water-ice', 'melting temperature': 0.}


class PDEInputs:
    exe_path = '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem'
    working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\run\\'
    end_time = 0.01
    time_step = 0.002
    max_cells = 1000
    dirichlet_boundary_ids = [5, 6, 7, 8, 9]
    dirichlet_boundary_values = [1.0, 0.1, 0.1, 0.1, 1.0]
    neumann_boundary_ids = [0, 1, 2, 3, 4]
    neumann_boundary_values = [-1.0, -1.0, -1.0, -1.0, -1.0]