
class TrajectoryInputs:
    name = 'default'
    step_count = 3
    # @todo: Generalize the plot view window
    plot_xlim = [-1., 1.]
    plot_ylim = [-1.5, 1.5]


class BodyInputs:
    geometry_name = 'hemisphere_cylinder_shell'
    sphere_radius = 0.25
    cylinder_length = 1.0
    arc_point_count = 11
    line_point_count = 11
    reference_length = sphere_radius


class EnvironmentInputs:
    temperature = -1.
    material = {'name': 'water-ice', 'melting temperature': 0.}


class PDEInputs:
    exe_path = '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem'
    working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\run\\'
    semi_implicit_theta = 1.0
    end_time = 0.01
    time_step = 0.002
    max_cells = 1000
    hot = 1.0
    warm = 0.1
    cold = -1.0
    dirichlet_boundary_ids = [5, 7, 9]
    dirichlet_boundary_values = [hot, warm, hot]
    neumann_boundary_ids = [0, 1, 2, 3, 4]
    neumann_boundary_values = [cold, cold, cold, cold, cold]
    dirichlet_ramp_boundary_ids = [6, 8]
    dirichlet_ramp_start_values = [hot, hot]
    dirichlet_ramp_end_values = [warm, warm]
    def __init__(self, body):
        R = body.input.sphere_radius
        L = body.input.cylinder_length
        self.sizes = [R, 4*R, L, 2*L]
        # @todo: Generalize handling of Dirichlet ramp boundaries
        self.dirichlet_ramp_start_points = [R, 0.,
                                           -R, 0.]
        self.dirichlet_ramp_end_points = [R, L,
                                         -R, L]

