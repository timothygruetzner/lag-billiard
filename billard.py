from tkinter import *


class Wall:
    def __init__(self):
        self.x_start = 0
        self.y_start = 0
        self.x_end = 0
        self.y_end = 0
        self.line_id = 0

window = Tk()
window.geometry("600x900")
wallCounter = 0
walls = []

def pressed(event):
    walls.append(Wall())
    walls[wallCounter].x_start = event.x
    walls[wallCounter].y_start = event.y


def moved(event):
    if walls[wallCounter].line_id != 0:
        c.delete(walls[wallCounter].line_id)
    walls[wallCounter].line_id = c.create_line(walls[wallCounter].x_start, walls[wallCounter].y_start, event.x, event.y)

def released(event):
    global wallCounter
    walls[wallCounter].x_end = event.x
    walls[wallCounter].y_end = event.y
    wallCounter += 1


window.bind("<Button-1>", pressed)
window.bind("<B1-Motion>", moved)
window.bind("<ButtonRelease-1>", released)

c = Canvas(window, width = 600, height=900)
c.pack()
window.mainloop()