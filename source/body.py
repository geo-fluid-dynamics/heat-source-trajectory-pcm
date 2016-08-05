import numpy as np
sphere_radius = 0.25
cylinder_length = 1.0
boundary_values = {'hot temperature': 1., 'warm temperature': 0.1}


def centroid(points):
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return sum_x/length, sum_y/length


def get_hull_points():
    # @todo: Add argument for number of discrete points and compute them based on the actual geometry.
    nose_tip = [0., -sphere_radius]
    body_points = np.array([nose_tip, [sphere_radius, 0], [sphere_radius, cylinder_length],
                            [-sphere_radius, cylinder_length], [-sphere_radius, 0], nose_tip])
    return body_points


def get_center_of_gravity():
    # Assume uniform density within the body
    body_points = get_hull_points()
    return centroid(body_points)
