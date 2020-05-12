import numpy as np


class Wall:
    def __init__(self):
        self.start = np.array([0, 0])
        self.end = np.array([0, 0])
        self.line_id = 0
        self.vector = np.empty([1, 2])
        self.last_intersection_coefficient = 0

    def calc_vector(self):
        # we define that start always is smaller than end
        self.vector = np.subtract(self.end, self.start)

    def intersect_is_in_bounds(self, intersection):
        if (intersection[0] < self.start[0] and intersection[0] > self.end[0]) or (
                intersection[0] > self.start[0] and intersection[0] < self.end[0]) or (
                intersection[1] > self.start[1] and intersection[1] < self.end[1]) or (
                intersection[1] < self.start[1] and intersection[1] > self.end[1]):
            return True
        return False
