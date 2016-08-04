import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pandas
import warnings


def get_field(state):
    solution_file_name = '../PDE/example_solution.vtk'
    warnings.warn("PDE solver not yet integrated; instead reading solution from "+solution_file_name)
    warnings.warn("Ignoring state "+str(state))
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    field = pandas.DataFrame(data=np.column_stack((nodes[:, 0], nodes[:, 1], u)),
                             columns=['XPosition', 'YPosition', 'Data'])
    field = field.drop_duplicates()
    return field


def test():
    field = get_field("../PDE/run/solution.0.10.vtk")
    print(field)


if __name__ == "__main__":
    test()
