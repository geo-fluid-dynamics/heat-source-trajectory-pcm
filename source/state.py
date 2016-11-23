import numpy as np

class State:
    def __init__(self):
        self.position = np.array((0., 0., 0.))
        self.orientation = np.array((0., 0., 0.))
        
    def __eq__(self, other):
        if not isinstance(other, State):
            return False

        if not all((self.get_position() == other.get_position())):
            return False

        if not all((self.get_orientation() == other.get_orientation())):
            return False

        return True    
        
    def __str__(self):
        return str({'position': self.position, 'orientation': self.orientation})
        
    def __add__(self, other):
        sum = State()
        sum.set_position(self.get_position() + other.get_position())
        sum.set_orientation(self.get_orientation() + other.get_orientation())
        return sum
    
    def __sub__(self, other):
        difference = State()
        difference.set_position(self.get_position() - other.get_position())
        difference.set_orientation(self.get_orientation() - other.get_orientation())
        return difference
    
    def __rmul__(self, factor):
        scaled = State()
        scaled.set_position(factor*self.get_position())
        scaled.set_orientation(factor*self.get_orientation())
        return scaled
    
    def set_position(self, position):
        assert(position.size == 3)
        self.position[:] = position
        
    def get_position(self):
        return self.position[:]
        
    def set_orientation(self, orientation):
        assert(orientation.size == 3)
        self.orientation[:] = orientation
        
    def get_orientation(self):
        return self.orientation[:]
        
        
if __name__ == "__main__":
    state = State()
    print(str(state))
    state2 = State()
    state2.set_position(np.array([0., 1., 0.]))
    assert((state2 - state) == state2)
    assert((state2 - state2) == state)
    
    state3 = 2*state2
    assert(state2 == 0.5*state3)