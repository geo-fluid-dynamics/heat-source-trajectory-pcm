import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas


def get_field(solution_file_name):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_name)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    field = pandas.DataFrame(data=np.column_stack((nodes[:, 0], nodes[:, 1], u)),
                             columns=['XPosition', 'YPosition', 'Data'])
    field = field.drop_duplicates()
    return field


def plot_interpolant(field):
    # Make interpolant using radial basis functions; this will be used for the constraints
    x = field['XPosition']
    y = field['YPosition']
    u = field['Data']
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    ui_grid = griddata(x, y, u, xi_grid, yi_grid)
    # plot the result
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.pcolor(xi_grid, yi_grid, ui_grid, cmap=cm.jet)
    plt.scatter(x, y, 10, u, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Natural neighbor interpolation')
    plt.colorbar()
    plt.show()


def test():
    field = get_field("../PDE/run/solution.0.10.vtk")
    plot_interpolant(field)


if __name__ == "__main__":
    test()
