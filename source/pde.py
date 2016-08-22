import vtk
from vtk.util.numpy_support import vtk_to_numpy
import math
import numpy as np
import pandas
from shutil import copyfile
import os
import subprocess
import fileinput
import shutil

import input
import trajectory

run_input_file_name = 'pde.prm'
end_time = input.pde['end_time']
time_step = input.pde['time_step']
pde_working_dir = input.pde['working_dir']

def init():
    if not os.path.exists(pde_working_dir):
        os.makedirs(pde_working_dir)
    with cd(pde_working_dir):
        bash_command = input.pde['exe_path'] # This will generate a default parameter file.
        subprocess.call('bash -c \''+bash_command+'\'')

def solve(step, state):
    with cd(pde_working_dir):
        # Prepare input file for PDE solver
        copyfile('default.prm', run_input_file_name)
        set_parameters(state)
        # Run the PDE solver
        bash_command = input.pde['exe_path']+' '+run_input_file_name
        subprocess.call('bash -c \''+bash_command+'\'')
    # Read the solution
    solution_file_name = 'solution-'+str(int(math.ceil(end_time/time_step)))+'.vtk'
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(pde_working_dir+solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    # Clean up the data
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    # Move some PDE solver outputs to archive directory
    archive_dir = pde_working_dir+'step'+str(step)+'\\'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    for file_name in ['log.txt', 'pde.prm']:
        shutil.move(os.path.join(pde_working_dir, file_name), os.path.join(archive_dir, file_name))
    for file in os.listdir(pde_working_dir):
        if file.endswith('.vtk'):
            shutil.move(os.path.join(pde_working_dir, file), os.path.join(archive_dir, file))
    return data


def set_parameters(state):
    parameters_to_set = {
        'sizes': [input.body['sphere_radius'], 2*input.body['sphere_radius'], input.body['cylinder_length'], 1.25*input.body['cylinder_length']],
        'transformations': [state[0], state[1], state[2]],
        'end_time' : end_time,
        'time_step' : time_step,
        'interpolate_old_field' : True,
        'max_cells' : input.pde['max_cells']
        }
    if all(state == trajectory.reference_state):
        parameters_to_set['interpolate_old_field'] = False
    for line in fileinput.input(files=run_input_file_name, inplace=1):
        for key, value in parameters_to_set.items():
            if key in line:
                line = '  set '+key+' = '+((str(value).lower()).replace("[", "")).replace("]", "")
        print(line.rstrip())


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def test():
    state = (0., 0., 0.)
    data = solve_pde(state)
    print(data)

if __name__ == "__main__":
    test()
