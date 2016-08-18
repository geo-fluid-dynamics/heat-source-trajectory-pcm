import fileinput
import trajectory
import pde
import body
reference_path = '../inputs/dimice.prm'
run_input_path = 'pde.prm'


def set_state(state):
    parameters_to_set = {'cylinder_outer_length' : 2*body.cylinder_length,
                         'sphere_outer_radius' : 6*body.sphere_radius,
                         'end_time' : pde.end_time,
                         'time_step' : pde.time_step,
                         'shift_along_x_axis' : state[0],
                         'shift_along_y_axis' : state[1],
                         'rotate_about_z_axis' : state[2],
                         'interpolate_old_field' : True,
                         'max_cells' : pde.max_cells
                        }
    if all(state == trajectory.reference_state):
        parameters_to_set['interpolate_old_field'] = False
    for line in fileinput.input(files=run_input_path, inplace=1):
        for key, value in parameters_to_set.items():
            if key in line:
                line = '  set '+key+' = '+str(value).lower()
        print(line.rstrip())
