import fileinput
reference_path = '../PDE/sphere-cylinder.prm'
run_input_path = 'pde.prm'


def set_state(state):
    point_value = state[:2]
    double_value = state[2]
    for line in fileinput.input(files=run_input_path, inplace=1):
        if 'set Optional double 5' in line:
            line = '  set Optional double 5 = '+str(double_value)
        elif 'set Optional Point 1' in line:
            line = '  set Optional Point 1 = '+str(point_value[0])+', '+str(point_value[1])
        line = line.rstrip()
        print(line)
