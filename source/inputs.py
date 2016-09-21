# @todo: Separate the geometry definitions of the body and the PDE field.


class TrajectoryInputs:
    def __init__(self):
        self.name = 'default'
        self.step_count = 5
        self.time_step_size = 0.02
        # @todo: Generalize the plot view window
        self.plot_xlim = [-1.5, 1.5]
        self.plot_ylim = [-3., 1.5]


class BodyInputs:
    def __init__(self):
        self.geometry_name = 'hyper_shell'
        self.sphere_radius = 1.
        self.reference_length = self.sphere_radius


class EnvironmentInputs:
    def __init__(self):
        self.temperature = -1.
        self.material = {'name': 'water-ice', 'melting temperature': 0.}


class PDEGeometryInputs:
    def __init__(self):
        self.grid_name = 'hyper_shell'
        self.sizes = [0.5, 1.]
        self.transformations = [0., 0., 0.]


class PDERefinementInputs:
    def __init__(self):
        self.boundaries_to_refine = 0
        self.initial_boundary_cycles = 4
        self.initial_global_cycles = 2


class PDEBoundaryConditionsInputs:
    def __init__(self):
        self.implementation_types = ['natural', 'strong']
        self.function_names = ['constant', 'constant']
        self.function_double_arguments = [1., -1.]


class PDEInitialValuesInputs:
    def __init__(self):
        self.function_name = 'constant'
        self.function_double_arguments = [-1.]


class PDETimeInputs:
    def __init__(self):
        self.semi_implicit_theta = 0.7
        self.step_size = 0.001


class PDESolverInputs:
    def __init__(self):
        self.tolerance = 1.e-8
        self.normalize_tolerance = True


class PDEInputs:
    def __init__(self, body):
        self.exe_path = '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem'
        self.working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\run\\Trajectory\\'
        self.use_physical_diffusivity = True
        self.geometry = PDEGeometryInputs()
        self.refinement = PDERefinementInputs()
        self.bc = PDEBoundaryConditionsInputs()
        self.iv = PDEInitialValuesInputs()
        self.time = PDETimeInputs()
        self.solver = PDESolverInputs()
        r = body.input.sphere_radius
        self.geometry.sizes = [r, 2 * r]
