import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import warnings
import plots
import pandas
melt_temperature = 0


def get_data(state):
    solution_file_name = '../PDE/example_solution.vtk'
    warnings.warn("PDE solver not yet integrated; instead reading solution from "+solution_file_name)
    warnings.warn("Ignoring state "+str(state))
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    return data


def test():
    state = (0., 0., 0.)
    data = get_data(state)
    plots.plot_inv_dist_kd_tree_interpolant(data)

if __name__ == "__main__":
    test()
