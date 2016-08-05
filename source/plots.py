from scipy.interpolate import Rbf
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import invdisttree


def grid_sample_points(data):
    # Interpolate data on to structured grid
    x = data[:, 0]
    y = data[:, 1]
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    return xi_grid, yi_grid


def plot_interpolant_and_data(xi_grid, yi_grid, ui_grid, data):
    # Plot the structured sample
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.pcolor(xi_grid, yi_grid, ui_grid, cmap=cm.jet)
    plt.scatter(data[:, 0], data[:, 1], 10, data[:, 2], cmap=cm.jet)
    plt.axis('equal')
    plt.colorbar()


def plot_inv_dist_kd_tree_interpolant(data):
    interpolant = invdisttree.Invdisttree(data[:, :2], data[:, 2])
    xi_grid, yi_grid = grid_sample_points(data)
    ui_grid = interpolant(np.column_stack((xi_grid.flatten(), yi_grid.flatten())))
    plot_interpolant_and_data(xi_grid, yi_grid, ui_grid.reshape(xi_grid.shape), data)
    plt.title('Inverse-distance KD-Tree interpolation')
    plt.draw()


def plot_nn_interpolant(data):
    xi_grid, yi_grid = grid_sample_points(data)
    ui_grid = griddata(data[:,0], data[:, 1], data[:, 2], xi_grid, yi_grid)  # Natural neighbor interpolation
    plot_interpolant_and_data(xi_grid, yi_grid, ui_grid, data)
    plt.title('Natural neighbor interpolation')
    plt.draw()


def plot_rbf_interpolant(data):
    xi_grid, yi_grid = grid_sample_points(data)
    interpolant = Rbf(data[:, 0], data[:, 1], data[:, 2], function='multiquadric')
    ui_grid = interpolant(xi_grid, yi_grid)
    plot_interpolant_and_data(xi_grid, yi_grid, ui_grid, data)
    plt.title('Multiquadric RBF interpolation')
    plt.draw()
