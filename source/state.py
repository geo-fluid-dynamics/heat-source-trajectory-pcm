import numpy as np

class State:
    def __init__(self):
        self.position = np.array((0., 0., 0.))
        self.orientation = np.array((0., 0., 0.))
        self.velocity = np.array((0., 0., 0.))
    
    def set_position(self, position):
        assert(position.size == 3)
        self.position[:] = position
        
    def get_position(self):
        return self.position[:]
        
if __name__ == "__main__":
    state = State()
    print(state)