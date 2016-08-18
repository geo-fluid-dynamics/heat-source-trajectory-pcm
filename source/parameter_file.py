import fileinput
import trajectory
import body
reference_path = '../inputs/dimice.prm'
run_input_path = 'pde.prm'


def set_state(state):
    parameters_to_set = {'cylinder_outer_length' : 1.5*body.cylinder_length,
                         'end_time' : 0.015,
                         'time_step' : 0.001,
                         'shift_along_x_axis' : state[0],
                         'shift_along_y_axis' : state[1],
                         'rotate_about_z_axis' : state[2],
                         'interpolate_old_field' : True,
                         'max_cells' : 500
                        }
    if all(state == trajectory.reference_state):
        parameters_to_set['interpolate_old_field'] = False
    for line in fileinput.input(files=run_input_path, inplace=1):
        for key, value in parameters_to_set.items():
            if key in line:
                line = '  set '+key+' = '+str(value).lower()
        print(line.rstrip())
