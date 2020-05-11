import numpy as np


class Wall:
    def __init__(self):
        self.start = np.array([0, 0])
        self.end = np.array([0, 0])
        self.line_id = 0
        self.vector = np.empty([1, 2])

    def calc_vector(self):
        self.vector = np.subtract(self.end, self.start)
