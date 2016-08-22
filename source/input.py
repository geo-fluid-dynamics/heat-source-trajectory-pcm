trajectory = {
    'step_count': 3
    }

body = {
    'sphere_radius': 0.25,
    'cylinder_length': 1.0,
    'boundary_values': {'hot temperature': 1., 'warm temperature': 0.1},
    'nose_arc_point_count': 11
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
    'max_cells': 500
    }