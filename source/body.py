import numpy as np
import math
sphere_radius = 0.25
cylinder_length = 1.0
boundary_values = {'hot temperature': 1., 'warm temperature': 0.1}


def move(old_points, x):
    assert(x.size == 3)  # 2D
    theta = x[2]
    rotation_matrix = np.matrix([[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]])
    # @todo: Is the rotation direction consistent with the deal.II parameter?
    points = np.matrix(old_points)*rotation_matrix
    points = points + x[:2]
    return np.array(points)


def centroid(points):
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return np.array((sum_x/length, sum_y/length))


def get_hull_points(state=np.array((0., 0., 0.))):
    # @todo: Add argument for number of discrete points and compute them based on the actual geometry.
    nose_tip = [0., -sphere_radius]
    body_points = np.array([nose_tip, [sphere_radius, 0], [sphere_radius, cylinder_length],
                            [-sphere_radius, cylinder_length], [-sphere_radius, 0]])
    body_points = move(body_points, state)
    return body_points


def get_center_of_gravity(state=np.array(0.)):
    return centroid(get_hull_points(state))  # Assume uniform density within the body


def close_curve(points):
    return np.row_stack((points, points[0, :]))
