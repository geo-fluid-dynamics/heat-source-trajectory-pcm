import numpy as np


def grid_sample_points(data):
    # Interpolate data on to structured grid
    x = data[:, 0]
    y = data[:, 1]
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    return xi_grid, yi_grid
