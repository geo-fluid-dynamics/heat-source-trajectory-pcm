import matplotlib.pyplot as plt
import numpy as np
import body


def plot_frame(traj, file_path):     
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    
    points = body.close_curve(traj.body.get_hull_points(traj.old_state))
    x = points[:, 0]
    y = points[:, 1]
    plt.plot(x, y, '--y', label='Old State')
    
    points = body.close_curve(traj.body.get_hull_points(traj.state))
    plt.plot(points[:, 0], points[:, 1], '-r', label='Current State')
    
    x_length = abs(max(x) - min(x))
    y_length = abs(max(y) - min(y))
    length = max((x_length, y_length))
    xlim = [min(x) - length, max(x) + length]
    plt.xlim(xlim)
    ylim = [min(y) - length, max(y) + length]
    plt.ylim(ylim)

    ni = 1000
    xi = np.linspace(xlim[0], xlim[1], ni)
    yi = np.linspace(ylim[0], ylim[1], ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    # @todo: Also shift in X direction 
    delta_y = traj.state.get_position()[1] - traj.pde.state.get_position()[1]
    ui = traj.pde.interpolator(xi_grid, yi_grid - delta_y)
    
    cp = plt.contour(xi_grid, yi_grid, ui.reshape(xi_grid.shape),
                     (0.8*traj.environment.temperature,
                     traj.environment.material['melting temperature']),
                     colors=('k', 'b'))
    plt.clabel(cp, inline=True, fontsize=10)
    
    plt.legend()
    plt.title('Step '+str(traj.step))
    plt.savefig(file_path)
    plt.cla()
    

# @todo: plot frames with ParaView
