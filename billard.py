from tkinter import *
from wall import Wall

window = Tk()
window.title("Python Billiard")
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


window.bind("<Button-3>", pressed)
window.bind("<B3-Motion>", moved)
window.bind("<ButtonRelease-3>", released)

c = Canvas(window, width=600, height=900)
c.configure(background="#0a6c03")

ball = c.create_oval(20, 20, 40, 40, outline="#000", fill="#fff", width=2)

c.pack()
window.mainloop()
