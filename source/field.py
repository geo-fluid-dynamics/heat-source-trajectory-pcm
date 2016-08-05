import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pandas
from shutil import copyfile
import parameter_file
import subprocess


temperature = -1.
material = {'name': 'water-ice', 'melting temperature': 0.}


def solve_pde(state):
    # Prepare input file for PDE solver
    copyfile(parameter_file.reference_path, parameter_file.run_input_path)
    parameter_file.set_state(state)
    # Run the PDE solver
    subprocess.check_output(['../pde/dimice-heat', parameter_file.run_input_path])  # Used check_output to silence
    # Read the solution
    solution_file_path = 'solution.0.1.vtk'
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_path)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    # Clean up the data
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    return data


def test():
    state = (0., 0., 0.)
    data = solve_pde(state)
    print(data)

if __name__ == "__main__":
    test()
