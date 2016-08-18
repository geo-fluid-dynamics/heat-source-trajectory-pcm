import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pandas
from shutil import copyfile
import parameter_file
import os
import subprocess


temperature = -1.
material = {'name': 'water-ice', 'melting temperature': 0.}
dimice_working_dir = 'C:\\Users\\Alexander\\UbuntuShared\\dimice-heat-dealii\\run\\'

def solve_pde(state):
    with cd(dimice_working_dir):
        # Prepare input file for PDE solver
        copyfile(parameter_file.reference_path, parameter_file.run_input_path)
        parameter_file.set_state(state)
        # Run the PDE solver
        bash_command = '../bin/heat_problem '+parameter_file.run_input_path
        subprocess.call('bash -c \''+bash_command+'\'')
        #subprocess.check_output(['bash -c \'..\\bin\\heat\'', parameter_file.run_input_path])  # Used check_output to silence
    # Read the solution
    # @todo: Read latest solution time instead of having to specify the exact file name here.
    solution_file_name = 'solution-15.vtk'
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(dimice_working_dir+solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    # Clean up the data
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    return data

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
