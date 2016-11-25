import vtk
from vtk.util.numpy_support import vtk_to_numpy
import math
import numpy as np
import pandas
import fileinput
import os
import os.path
import subprocess
import shutil
from scipy import interpolate

import state  

class Geometry:

    def __init__(self):
        self.dim = 2
        self.grid_name = 'hyper_shell'
        self.sizes = [0.5, 1.]
        self.transformations = [0., 0., 0.]
        
        
class Refinement:

    def __init__(self):
        self.boundaries_to_refine = 0
        self.initial_boundary_cycles = 4
        self.initial_global_cycles = 2
        
        
class BoundaryConditions:

    def __init__(self):
        self.implementation_types = ['natural', 'strong']
        self.function_names = ['constant', 'constant']
        self.function_double_arguments = [1., -1.]
        

class InitialValues:

    def __init__(self):
        self.function_name = 'constant'
        self.function_double_arguments = [-1.]
        
        
class Time:
    def __init__(self):
        self.semi_implicit_theta = 0.7
        self.step_size = 0.001


class Solver:
    def __init__(self):
        self.tolerance = 1.e-8
        self.normalize_tolerance = True

        
class PDE:

    def __init__(self, geometry):
        self.geometry = Geometry()
        self.refinement = Refinement()
        self.bc = BoundaryConditions()
        self.iv = InitialValues()
        self.time = Time()
        self.solver = Solver()
        
        self.exe_path = '/home/zimmerman/dimice-pde-dealii/build/heat_problem'
        self.use_physical_diffusivity = False
        self.enable_convection = True
        
        self.state = state.State()
        self.state_dot = state.State()
        self.run_input_file_name = 'pde.prm'
        self.interpolate_old_field = False
        self.data = []
        self.interpolator = []
        
        
    def solve(self, trajectory):

        self.write_parameters(trajectory.time_step_size)

        # Run the PDE solver
        subprocess.call([self.exe_path, self.run_input_file_name])

        # Read the solution
        solution_file_name = \
            'solution-'+str(int(math.ceil(trajectory.time_step_size/self.time.step_size)))+'.vtk'
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(solution_file_name)
        reader.Update()
        nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
        u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
        # Clean up the data
        data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
        table = pandas.DataFrame(data=data)
        table = table.drop_duplicates()
        self.data = table.as_matrix()
        #
        self.interpolator = interpolate.LinearNDInterpolator(
            data[:, :2], data[:, 2], fill_value=trajectory.environment.temperature)

        # Move some PDE solver outputs to archive directory
        archive_dir = trajectory.name+'/'
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        for file_name in [self.run_input_file_name]:
            shutil.move(
                os.path.join('.', file_name),
                os.path.join(archive_dir, 'step'+str(trajectory.step)+'_'+file_name))

        for f in os.listdir('.'):
            if f.endswith('.vtk'):
                pde_step_count = round(trajectory.time_step_size/self.time.step_size)
                old_solution_number = int((f.replace('.vtk', '')).replace('solution-', ''))
                solution_number = int(pde_step_count*trajectory.step + old_solution_number + trajectory.step)
                new_file = 'solution-'+str(solution_number)+'.vtk'
                shutil.move(os.path.join('.', f), os.path.join(archive_dir, new_file))

    def write_parameters(self, end_time):

        if self.interpolate_old_field:
            iv_function_name = 'interpolate_old_field'
        else:
            iv_function_name = 'constant'
        
        parameters = {
            'pde': {
                'use_physical_diffusivity': self.use_physical_diffusivity,
                'convection_velocity': [self.state_dot.get_position()[0], self.state_dot.get_position()[1]]},
            'geometry': {
                'dim': self.geometry.dim,
                'grid_name': self.geometry.grid_name,
                'sizes': self.geometry.sizes,
                'transformations': [self.state.get_position()[0], self.state.get_position()[1], self.state.get_orientation()[0]]},
            'refinement': {
                'boundaries_to_refine': self.refinement.boundaries_to_refine,
                'initial_boundary_cycles': self.refinement.initial_boundary_cycles,
                'initial_global_cycles': self.refinement.initial_global_cycles},
            'boundary_conditions': {
                'implementation_types': self.bc.implementation_types,
                'function_names': self.bc.function_names,
                'function_double_arguments': self.bc.function_double_arguments},
            'initial_values': {
                'function_name': iv_function_name,
                'function_double_arguments': self.iv.function_double_arguments},
            'time': {
                'semi_implicit_theta': self.time.semi_implicit_theta,
                'time_step': self.time.step_size,
                'end_time': end_time},
            'solver': {
                'tolerance': self.solver.tolerance,
                'normalize_tolerance': self.solver.normalize_tolerance
                }
            }

        param_file = open(self.run_input_file_name, 'w')

        for subsection_key, subsection_dict in parameters.items():
            param_file.write('\n' + 'subsection ' + subsection_key + '\n\n')
            for key, value in subsection_dict.items():
                param_file.write('    set ' + key + ' = ' + strip_brackets_and_quotations(str(value).lower()) + '\n')
            param_file.write('\n' + 'end' + '\n\n')

        param_file.close()

        assert(os.path.isfile(self.run_input_file_name))


def replace_parameter(file_name, subsection_key, key, value):
    found_subsection_key = False
    found_key = False
    for line in fileinput.input(files=file_name, inplace=1):
        if 'subsection '+subsection_key in line:
            found_subsection_key = True
        if found_subsection_key & 'set '+key in line:
            found_key = True
            line = '  set '+key+' = '+strip_brackets_and_quotations(str(value).lower())
        print(line.rstrip())
    if not found_subsection_key:
        raise NameError(subsection_key)
    if not found_key:
        raise NameError(key)


def strip_brackets_and_quotations(string):
    for bracket_or_quote in ('[', ']', '(', ')', "'", '"'):
        string = string.replace(bracket_or_quote, '')
    return string


class cd:
        """Context manager for changing the current working directory"""
        def __init__(self, new_path):
            self.new_path = os.path.expanduser(new_path)

        def __enter__(self):
            self.saved_path = os.getcwd()
            os.chdir(self.new_path)

        def __exit__(self, exit_type, value, traceback):
            os.chdir(self.saved_path)


if __name__ == "__main__":
    # @todo: Write a test that runs the default PDE problem.
    # As of writing this comment, the issue is that the solve() method requires a Trajectory instance as input.
    raise Exception('This module has no main program.')
