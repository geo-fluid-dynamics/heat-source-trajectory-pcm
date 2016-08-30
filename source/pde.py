import vtk
from vtk.util.numpy_support import vtk_to_numpy
import math
import numpy as np
import pandas
import shutil
import os
import subprocess
import fileinput
import shutil
import scipy

import inputs


class PDE:

    default_parameter_file_name = 'default.prm'

    def __init__(self, body):
        self.input = inputs.PDEInputs(body)
        self.body = body
        self.run_input_file_name = 'pde.prm'
        self.interpolate_old_field = False
        self.data = []
        self.interpolator = []
        if not os.path.exists(self.input.working_dir):
            os.makedirs(self.input.working_dir)
        with cd(self.input.working_dir):
            # Clean the working dir
            if os.path.exists(self.default_parameter_file_name):
                os.remove(self.default_parameter_file_name)
            # Generate the default parameter file.
            command = 'bash -c \''+self.input.exe_path+'\''
            subprocess.call(command)


    def solve(self, trajectory):
        with cd(self.input.working_dir):
            # Prepare input file for PDE solver
            shutil.copyfile(self.default_parameter_file_name, self.run_input_file_name)
            self.set_parameters(trajectory.state)
            # Run the PDE solver
            bash_command =self.input.exe_path+' '+self.run_input_file_name
            subprocess.call('bash -c \''+bash_command+'\'')
        # Read the solution
        solution_file_name = 'solution-'+str(int(math.ceil(self.end_time/self.input.time_step)))+'.vtk'
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
        self.interpolator = scipy.interpolate.LinearNDInterpolator(data[:, :2], data[:, 2],
                                                                   fill_value=trajectory.environment.temperature)
        # Move some PDE solver outputs to archive directory
        archive_dir = self.input.working_dir+trajectory.input.name+'\\'
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        for file_name in ['log.txt', 'pde.prm']:
            shutil.move(os.path.join(self.input.working_dir, file_name), 
                os.path.join(archive_dir, 'step'+str(trajectory.step)+'_'+file_name))
        for file in os.listdir(self.input.working_dir):
            if file.endswith('.vtk'):
                pde_step_count = round(trajectory.input.time_step/self.input.time_step)
                old_solution_number = int((file.replace('.vtk', '')).replace('solution-', ''))
                solution_number = int(pde_step_count*trajectory.step + old_solution_number)
                new_file = 'solution-'+str(solution_number)+'.vtk'
                shutil.move(os.path.join(self.input.working_dir, file),
                    os.path.join(archive_dir, new_file))


    def set_parameters(self, state):
        assert(self.body.input.geometry_name == 'hyper_shell')
        parameters_to_set = {
            'sizes': self.input.sizes,
            'transformations': [state[0], state[1], state[2]],
            'semi_implicit_theta': self.input.semi_implicit_theta,
            'end_time': self.end_time,
            'time_step': self.input.time_step,
            'interpolate_old_field': self.interpolate_old_field,
            'initial_boundary_refinement': self.input.initial_boundary_refinement,
            'n_adaptive_pre_refinement_steps': self.n_adaptive_pre_refinement_steps,
            'max_cells': self.input.max_cells,
            'dirichlet_boundary_ids': self.input.dirichlet_boundary_ids,
            'dirichlet_boundary_values': self.input.dirichlet_boundary_values,
            'neumann_boundary_ids': self.input.neumann_boundary_ids,
            'neumann_boundary_values': self.input.neumann_boundary_values,
            }
        for key, value in parameters_to_set.items():
            set_parameter(self.run_input_file_name, key, value)
    

    def test(self):
        state = (0., 0., 0.)
        data = solve_pde(0, state, state)
        print(data)


def set_parameter(file_name, key, value):
    found_key = False
    for line in fileinput.input(files=file_name, inplace=1):
        if 'set '+key in line:
            found_key = True
            line = '  set '+key+' = '+strip_brackets(str(value).lower())
        print(line.rstrip())
    if not found_key:
        raise NameError(key)


def strip_brackets(string):
    for bracket in ('[', ']', '(', ')'):
        string = string.replace(bracket, '')
    return string


class cd:
        """Context manager for changing the current working directory"""
        def __init__(self, newPath):
            self.newPath = os.path.expanduser(newPath)

        def __enter__(self):
            self.savedPath = os.getcwd()
            os.chdir(self.newPath)

        def __exit__(self, etype, value, traceback):
            os.chdir(self.savedPath)


if __name__ == "__main__":
    pde = PDE()
    pde.test()
