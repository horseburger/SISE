import numpy as np
from random import choice

class Model:
    def __init__(self):
        self.target_state = np.array([[1, 2, 3, 4],
                                      [5, 6, 7, 8],
                                      [9, 10, 11, 12],
                                      [13, 14, 15, 0]])
        
        self.current_state, self.zero_position = self.__generate_state()

    # generates the random 15-puzzle starting state
    # returns a tuple (random state, position of the 0 element)
    def __generate_state(self):
        numbers = list(range(16))
        state = np.array([[-1, -1, -1, -1] for i in range(4)])
        while numbers:
            for i in range(4):
                for j in range(4):
                    if state[i, j] == -1:
                        tmp = choice(numbers)
                        if not tmp:
                            zero = (i, j)
                        state[i, j] = tmp
                        numbers.remove(tmp)

        return state, zero

    def __swap(self, a, b):
        tmp = self.current_state[a]
        self.current_state[a] = self.current_state[b]
        self.current_state[b] = tmp

    def get_neighbour_states(self):
        tmp = []
        if self.zero_position[0]:
            tmp.append('U')
        if self.zero_position[1]:
            tmp.append('L')
        if self.zero_position[0] != 3:
            tmp.append('D')
        if self.zero_position[1] != 3:
            tmp.append('R')
        return tmp

    def is_solved(self):
        return np.array_equal(self.current_state, self.target_state)

    def __str__(self):
        return """Current state:\n {}\n\nZero position:\n{}\n""".format(self.current_state, self.zero_position)
                        

if __name__ == '__main__': 
    m = Model()