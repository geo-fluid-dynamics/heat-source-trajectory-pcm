from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def plot_interpolant(field):
    # Interpolate data on to structured grid
    x = field['XPosition']
    y = field['YPosition']
    u = field['Data']
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    ui_grid = griddata(x, y, u, xi_grid, yi_grid) # Natural neighbor interpolation
    # Plot the structured sample
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.pcolor(xi_grid, yi_grid, ui_grid, cmap=cm.jet)
    plt.scatter(x, y, 10, u, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Natural neighbor interpolation')
    plt.colorbar()
    plt.show()
