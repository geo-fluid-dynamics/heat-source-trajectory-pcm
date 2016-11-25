import matplotlib.pyplot as plt
import numpy as np
import body

def grid_sample_points(data):
    # Interpolate data on to structured grid
    x = data[:, 0]
    y = data[:, 1]
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    return xi_grid, yi_grid
    

def plot_frame(traj, file_path):     
    xi_grid, yi_grid = grid_sample_points(traj.pde.data)
    
    delta_y = traj.state.get_position()[1] - traj.pde.state.get_position()[1]
    ui = traj.pde.interpolator(xi_grid, yi_grid - delta_y)
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    cp = plt.contour(xi_grid, yi_grid, ui.reshape(xi_grid.shape),
                     (0.8*traj.environment.temperature,
                     traj.environment.material['melting temperature']),
                     colors=('k', 'b'))
    plt.clabel(cp, inline=True, fontsize=10)
    points = body.close_curve(traj.body.get_hull_points(traj.old_state))
    plt.plot(points[:, 0], points[:, 1], '--y', label='Old State')
    
    points = body.close_curve(traj.body.get_hull_points(traj.state))
    x = points[:, 0]
    y = points[:, 1]
    plt.plot(x, y, '-r', label='Current State')
    
    x_length = abs(max(x) - min(x))
    y_length = abs(max(y) - min(y))
    plt.xlim([min(x) - x_length, max(x) + x_length])
    plt.ylim([min(y) - y_length, max(y) + y_length])
    
    plt.legend()
    plt.title('Step '+str(traj.step))
    plt.savefig(file_path)
    plt.cla()
    

# @todo: plot frames with ParaView
