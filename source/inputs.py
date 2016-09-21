
class TrajectoryInputs:
    name = 'default'
    step_count = 5
    time_step = 0.02
    # @todo: Generalize the plot view window
    plot_xlim = [-1.5, 1.5]
    plot_ylim = [-3., 1.5]


class BodyInputs:
    geometry_name = 'hyper_shell'
    sphere_radius = 1.
    reference_length = sphere_radius


class EnvironmentInputs:
    temperature = -1.
    material = {'name': 'water-ice', 'melting temperature': 0.}


class PDEInputs:
    exe_path = '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem'
    working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\run\\'
    semi_implicit_theta = 0.7
    time_step = 0.001
    max_cells = 10000
    initial_boundary_refinement = 5
    initial_global_refinement = 0
    n_adaptive_pre_refinement_steps = 0
    refinement_interval = 0
    n_refinement_cycles = 0
    refine_fraction = 0.6
    dirichlet_boundary_ids = [1]
    dirichlet_boundary_values = [-1.]
    neumann_boundary_ids = [0]
    neumann_boundary_values = [10.]
    def __init__(self, body):
        R = body.input.sphere_radius
        self.sizes = [R, 2*R]

