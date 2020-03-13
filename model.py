import numpy as np
from random import randint, choice

class Model:
    def __init__(self, search_order="LRUD", heuristic=None):
        self.target_state = np.array([[1, 2, 3, 4],
                                      [5, 6, 7, 8],
                                      [9, 10, 11, 12],
                                      [13, 14, 15, 0]], np.int8)
        
        # placeholders for the vars to improve code readability, used in __generate_state()
        self.current_state = None
        self.zero_position = None
        self.search_order = search_order
        self.heuristic = heuristic

        self.__generate_state()

    # generates the random 15-puzzle starting state
    def __generate_state(self):
        self.current_state = np.copy(self.target_state)
        self.zero_position = (3, 3)

        # number of operations mixing the state
        for i in range(randint(5, 15)):
            op = choice(self.get_operators())
            self.current_state, self.zero_position = self.get_neighbour_state(op)

    def __swap(self, a, new_state):
        a = tuple(a)
        tmp = new_state[self.zero_position]
        new_state[self.zero_position] = new_state[a]
        new_state[a] = tmp

    def get_operators(self):
        allowed = []

        if self.zero_position[0]:
            allowed.append('U')
        if self.zero_position[1]:
            allowed.append('L')
        if self.zero_position[0] != 3:
            allowed.append('D')
        if self.zero_position[1] != 3:
            allowed.append('R')
        

        return [char for char in self.search_order.upper() if char in allowed]


    # return the new state as a numpy 2dim array and the position of 0 in the array
    def get_neighbour_state(self, operator):
        
        new_state = np.copy(self.current_state)

        if operator == 'U':
            tmp = list(self.zero_position)
            tmp[0] -= 1
            self.__swap(tmp, new_state)
        
        if operator == 'L':
            tmp = list(self.zero_position)
            tmp[1] -= 1
            self.__swap(tmp, new_state)

        if operator == 'D':
            tmp = list(self.zero_position)
            tmp[0] += 1
            self.__swap(tmp, new_state)

        if operator == 'R':
            tmp = list(self.zero_position)
            tmp[1] += 1
            self.__swap(tmp, new_state)
        

        return new_state, tuple(tmp)

    def is_solved(self):
        return np.array_equal(self.current_state, self.target_state)

    def __str__(self):
        return """Current state:\n {}\n\nZero position:\n{}\n""".format(self.current_state, self.zero_position)
                        

if __name__ == '__main__': 
    m = Model()