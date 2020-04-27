import numpy as np
from random import randint, choice


class Model:
    def __init__(self, search_order="LRUD", heuristic=None, search_strategy="hamm"):
        self.target_state = np.array([[1, 2, 3, 4],
                                      [5, 6, 7, 8],
                                      [9, 10, 11, 12],
                                      [13, 14, 15, 0]], np.int8)

        # placeholders for the vars to improve code readability, used in __generate_state()
        self.current_state = None
        self.zero_position = None
        self.first_state = None
        self.first_zero = None
        self.search_order = search_order
        self.search_strategy = search_strategy
        self.heuristic = heuristic

        self.__generate_state()

    # generates the random 15-puzzle starting state
    def __generate_state(self):
        self.current_state = np.copy(self.target_state)
        self.zero_position = (3, 3)

        # number of operations mixing the state
        for i in range(7):
            op = choice(self.get_operators())
            self.current_state, self.zero_position = self.get_neighbour_state(
                op)

        self.current_state = self.current_state.astype(np.int8)
        self.first_state = np.copy(self.current_state)
        self.first_zero = self.zero_position

    def load_layout(self, dimensions, layout):
        state = np.array([[-1]*dimensions[0]
                          for _ in range(dimensions[1])], np.int8)
        mod = dimensions[0] * dimensions[1]
        for i in range(mod):
            if not layout[i]:
                self.zero_position = (i // dimensions[0], i % dimensions[1])
            state[i // dimensions[0], i % dimensions[1]] = layout[i]

        self.current_state = np.copy(state)
        self.first_state = np.copy(state)
        self.first_zero = self.zero_position

    def __swap(self, a, new_state):
        new_state[self.zero_position], new_state[tuple(
            a)] = new_state[tuple(a)], new_state[self.zero_position]

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

    def is_solved(self, state):
        return np.array_equal(self.target_state, state)

    def get_f_value(self, next_state, depth):
        if self.search_strategy == "hamm":
            current = next_state.flatten()
            target = self.target_state.flatten()
            value = 0
            for x in range(0, 15):
                if(current[x] != target[x]):
                    value += 1
            return value

        elif self.search_strategy == "manh":
            current = dict((j, (x, y)) for x, i in enumerate(next_state) for y, j in enumerate(i))
            target = dict((j, (x, y)) for x, i in enumerate(self.target_state) for y, j in enumerate(i))
            value = 0
            for x in range(0, 15):
                value += abs(current[x][0] - target[x][0]) + abs(current[x][1] - target[x][1])
            return value

    def __str__(self):
        return """Current state:\n {}\n\nZero position:\n{}\n""".format(self.current_state, self.zero_position)


if __name__ == '__main__':
    m = Model()
