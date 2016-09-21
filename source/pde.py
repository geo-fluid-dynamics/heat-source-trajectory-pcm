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
import scipy

import inputs


class PDE:

    def __init__(self, body):
        self.input = inputs.PDEInputs(body)
        self.body = body
        self.run_input_file_name = 'pde.prm'
        self.interpolate_old_field = False
        self.data = []
        self.interpolator = []
        if not os.path.exists(self.input.working_dir):
            os.makedirs(self.input.working_dir)

    def solve(self, trajectory):
        with cd(self.input.working_dir):
            self.write_parameters(trajectory.state, trajectory.input.time_step_size)
            # Run the PDE solver
            bash_command = self.input.exe_path+' '+self.run_input_file_name
            subprocess.call('bash -c \''+bash_command+'\'')
        # Read the solution
        solution_file_name = \
            'solution-'+str(int(math.ceil(trajectory.input.time_step_size/self.input.time.step_size)))+'.vtk'
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(self.input.working_dir+solution_file_name)
        reader.Update()
        nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
        u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
        # Clean up the data
        data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
        table = pandas.DataFrame(data=data)
        table = table.drop_duplicates()
        self.data = table.as_matrix()
        #
        self.interpolator = scipy.interpolate.LinearNDInterpolator(
            data[:, :2], data[:, 2], fill_value=trajectory.environment.temperature)

        # Move some PDE solver outputs to archive directory
        archive_dir = self.input.working_dir+trajectory.input.name+'\\'
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        for file_name in ['solution_table.txt', self.run_input_file_name]:
            shutil.move(
                os.path.join(self.input.working_dir, file_name),
                os.path.join(archive_dir, 'step'+str(trajectory.step)+'_'+file_name))

        for f in os.listdir(self.input.working_dir):
            if f.endswith('.vtk'):
                pde_step_count = round(trajectory.input.time_step_size/self.input.time.step_size)
                old_solution_number = int((f.replace('.vtk', '')).replace('solution-', ''))
                solution_number = int(pde_step_count*trajectory.step + old_solution_number)
                new_file = 'solution-'+str(solution_number)+'.vtk'
                shutil.move(os.path.join(self.input.working_dir, f), os.path.join(archive_dir, new_file))

    def write_parameters(self, state, end_time):

        if self.interpolate_old_field:
            iv_function_name = 'interpolate_old_field'
        else:
            iv_function_name = 'constant'
        
        parameters = {
            'pde': {
                'use_physical_diffusivity': self.input.use_physical_diffusivity,
                'convection_velocity': state.velocity},
            'geometry': {
                'dim': self.input.geometry.dim,
                'grid_name': self.input.geometry.grid_name,
                'sizes': self.input.geometry.sizes,
                'transformations': [state.position[0], state.position[1], state.orientation[0]]},
            'refinement': {
                'boundaries_to_refine': self.input.refinement.boundaries_to_refine,
                'initial_boundary_cycles': self.input.refinement.initial_boundary_cycles,
                'initial_global_cycles': self.input.refinement.initial_global_cycles},
            'boundary_conditions': {
                'implementation_types': self.input.bc.implementation_types,
                'function_names': self.input.bc.function_names,
                'function_double_arguments': self.input.bc.function_double_arguments},
            'initial_values': {
                'function_name': iv_function_name,
                'function_double_arguments': self.input.iv.function_double_arguments},
            'time': {
                'semi_implicit_theta': self.input.time.semi_implicit_theta,
                'time_step': self.input.time.step_size,
                'end_time': end_time},
            'solver': {
                'tolerance': self.input.solver.tolerance,
                'normalize_tolerance': self.input.solver.normalize_tolerance
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
