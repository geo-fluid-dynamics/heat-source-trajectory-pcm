import numpy as np
import math

import inputs


class Body:

    def __init__(self):
        self.input = inputs.BodyInputs()

    def get_hull_points(self, state):
        points = make_sphere_points(self.input.sizes[0])
        points = move(points, state)
        return points

    def get_center_of_gravity(self, state):
        return centroid(self.get_hull_points(state))  # Assume uniform density within the body


def close_curve(points):
    return np.row_stack((points, points[0, :]))


def make_sphere_points(sphere_radius=1., point_count=33):
        # Construct spherical curve parametrically
        sample_angles = np.linspace(0, 2*np.pi, point_count)
        x = sphere_radius*np.cos(sample_angles)
        y = sphere_radius*np.sin(sample_angles)
        points = np.vstack((x, y))
        points = np.transpose(points)
        return points


def make_sphere_cylinder_points(sphere_radius=0.25, cylinder_length=1.0,
                                arc_point_count=5, line_point_count=5):
        # Construct spherical curve parametrically
        sample_angles = np.linspace(np.pi, 2*np.pi, arc_point_count)
        nose_x = sphere_radius*np.cos(sample_angles)
        nose_y = sphere_radius*np.sin(sample_angles)
        nose_points = np.vstack((nose_x, nose_y))
        nose_points = np.transpose(nose_points)
        # Construct cylinder
        aft_body_points = points_on_line([sphere_radius, 0], [sphere_radius, cylinder_length], line_point_count)
        aft_body_points = np.append(aft_body_points,
                                    points_on_line([-sphere_radius, cylinder_length], [-sphere_radius, 0],
                                                   line_point_count),
                                    axis=0)
        #
        body_points = np.concatenate((nose_points, aft_body_points))
        return body_points


def points_on_line(start_point, end_point, count):
    assert(len(start_point) == 2)  # 2D
    return np.transpose(np.vstack((np.linspace(start_point[0], end_point[0], count),
                                   np.linspace(start_point[1], end_point[1], count))))


def centroid(points):
    assert(points.shape[1] == 2)  # 2D
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return np.array((sum_x/length, sum_y/length))


def move(old_points, state):
    assert(state.orientation[1] == 0.)  # Only rotation about z axis is supported.
    assert(state.orientation[2] == 0.)  # Only rotation about z axis is supported.
    theta = state.orientation[0]
    rotation_matrix = np.matrix([[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]])
    points = np.matrix(old_points)*rotation_matrix
    points[:, 0] = points[:, 0]  + state.get_position()[0]
    points[:, 1] = points[:, 1]  + state.get_position()[1]
    return np.array(points)


if __name__ == "__main__":
    body = Body()
    print(body)