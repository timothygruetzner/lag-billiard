import numpy as np


class Ball:

    def __init__(self, canvas):
        self.canvas = canvas
        self.pos = np.array([50, 50])
        self.canvas_id = 0
        self.radix = 10

    def get_pos1(self):
        return np.array([self.pos[0] - (self.radix / 2), self.pos[1] - (self.radix / 2)])

    def get_pos2(self):
        return np.array([self.pos[0] + (self.radix / 2), self.pos[1] + (self.radix / 2)])

    def draw(self):
        if self.canvas_id != -1:
            self.canvas.delete(self.canvas_id)

        self.canvas_id = self.canvas.create_oval(self.get_pos1()[0], self.get_pos1()[1], self.get_pos2()[0],
                                                 self.get_pos2()[1], outline="#000",
                                                 fill="#fff", width=2)

    def move(self, dir_x, dir_y):
        self.canvas.move(self.canvas_id, dir_x, dir_y)
        self.pos = np.array([self.pos[0] + dir_x, self.pos[1] + dir_y])

    def moveTo(self, coords):
        self.pos = np.array([coords[0], coords[1]])
        self.draw()
