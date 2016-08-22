trajectory = {
    'step_count': 3
    }

inner_radius = 0.25
body = {
    'geometry_name': 'hemisphere_cylinder_shell',
    'sizes': [inner_radius, 1.25, 1.0, 2.0],
    'arc_point_count': 11,
    'reference_length': inner_radius
    }


field = {
    'temperature': -1.,
    'material': {'name': 'water-ice', 'melting temperature': 0.}
    }


pde = {
    'exe_path': '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem',
    'working_dir': 'C:\\Users\\Alexander\\UbuntuShared\\run\\',
    'end_time': 0.004,
    'time_step': 0.002,
    'max_cells': 500,
    'dirichlet_boundary_ids': [5, 6, 7, 8, 9],
    'dirichlet_boundary_values': [1.0, 0.1, 0.1, 0.1, 1.0],
    'neumann_boundary_ids': [0, 1, 2, 3, 4],
    'neumann_boundary_values': [-1.0, -1.0, -1.0, -1.0, -1.0]
    }