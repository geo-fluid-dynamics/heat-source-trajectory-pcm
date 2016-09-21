from collections import namedtuple

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


class PDEGeometryInputs:
    grid_name = 'hyper_shell'
    sizes = [0.5, 1.]
    transformations = [0., 0., 0.]

class PDETimeInputs:
    semi_implicit_theta = 0.7
    step_size = 0.001

class PDERefinementInputs:
    boundaries_to_refine = 0
    initial_boundary_cycles = 4
    initial_global_cycles = 2
    
class PDEBoundaryConditionsInputs:
    implementation_types = ['natural', 'strong']
    function_names = ['constant', 'constant']
    function_double_arguments = [1., -1.]
    
class PDEInitialValuesInputs:
    function_name = 'constant'
    function_double_arguments = [-1.]
    
class PDEInputs:
    exe_path = '/mnt/c/Users/Alexander/UbuntuShared/dimice-heat-dealii/bin/heat_problem'
    working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\run\\'
    geometry = PDEGeometryInputs()
    refinement = PDERefinementInputs()
    bc = PDEBoundaryConditionsInputs()
    iv = PDEInitialValuesInputs()
    time = PDETimeInputs()
    
    def __init__(self, body):
        R = body.input.sphere_radius
        self.geometry.sizes = [R, 2*R]

