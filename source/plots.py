from scipy import interpolate
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import invdisttree
import interpolate_structured


def plot_contour_and_data(xi_grid, yi_grid, ui_grid, data):
    # Plot the structured sample
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.pcolor(xi_grid, yi_grid, ui_grid, cmap=cm.jet)
    plt.scatter(data[:, 0], data[:, 1], 10, data[:, 2], cmap=cm.jet)
    plt.axis('equal')
    plt.colorbar()
    plt.draw()
    plt.show()


def plot_interpolator_and_data(interpolator, data):
    xi_grid, yi_grid = interpolate_structured.grid_sample_points(data)
    query_points = np.column_stack((xi_grid.flatten(), yi_grid.flatten()))
    ui = interpolator(query_points)
    plot_contour_and_data(xi_grid, yi_grid, ui.reshape(xi_grid.shape), data)


def plot_linear_spline_interpolant(data):
    interpolant = interpolate.interp2d(data[:, 0], data[:, 1], data[:, 2])
    # The documentation seems wrong: http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html
    # As far as I can tell, x and y must be vectors for the tensor product grid.
    n = 100
    xi = np.linspace(min(data[:, 0]), max(data[:, 0]), n)
    yi = np.linspace(min(data[:, 1]), max(data[:, 1]), n)
    ui_grid = interpolant(xi, yi)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    plot_contour_and_data(xi_grid, yi_grid, ui_grid, data)
    plt.title('Linear spline interpolation')
    plt.draw()
    plt.show()


def plot_inv_dist_kd_tree_interpolant(data):
    interpolant = invdisttree.Invdisttree(data[:, :2], data[:, 2])
    xi_grid, yi_grid = grid_sample_points(data)
    ui_grid = interpolant(np.column_stack((xi_grid.flatten(), yi_grid.flatten())))
    plot_contour_and_data(xi_grid, yi_grid, ui_grid.reshape(xi_grid.shape), data)
    plt.title('Inverse-distance KD-Tree interpolation')
    plt.draw()
    plt.show()


def plot_nn_interpolant(data):
    xi_grid, yi_grid = grid_sample_points(data)
    ui_grid = griddata(data[:, 0], data[:, 1], data[:, 2], xi_grid, yi_grid)  # Natural neighbor interpolation
    plot_contour_and_data(xi_grid, yi_grid, ui_grid, data)
    plt.title('Natural neighbor interpolation')
    plt.draw()


def plot_rbf_interpolant(data):
    xi_grid, yi_grid = grid_sample_points(data)
    interpolant = interpolate.Rbf(data[:, 0], data[:, 1], data[:, 2], function='multiquadric')
    ui_grid = interpolant(xi_grid, yi_grid)
    plot_contour_and_data(xi_grid, yi_grid, ui_grid, data)
    plt.title('Multiquadric RBF interpolation')
    plt.draw()
