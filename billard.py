from tkinter import *
import numpy as np
from wall import Wall

HEIGHT = 900
WIDTH = 600

window = Tk()
window.title("Python Billiard")
window.resizable(False, False)

moveOnGoing = False
wallCounter = 0
walls = []

# init walls around window
upperWall = Wall()
upperWall.x_start = 0
upperWall.y_start = 0
upperWall.x_end = WIDTH
upperWall.y_end = 0
walls.append(upperWall)
wallCounter += 1

rightWall = Wall()
rightWall.x_start = WIDTH
rightWall.y_start = 0
rightWall.x_end = WIDTH
rightWall.y_end = HEIGHT
walls.append(rightWall)
wallCounter += 1

lowerWall = Wall()
lowerWall.x_start = 0
lowerWall.y_start = HEIGHT
lowerWall.x_end = WIDTH
lowerWall.y_end = HEIGHT
walls.append(lowerWall)
wallCounter += 1

leftWall = Wall()
leftWall.x_start = 0
leftWall.y_start = 0
leftWall.x_end = 0
leftWall.y_end = HEIGHT
walls.append(leftWall)
wallCounter += 1


def rightPressed(event):
    walls.append(Wall())
    walls[wallCounter].x_start = event.x
    walls[wallCounter].y_start = event.y


def rightMoved(event):
    if walls[wallCounter].line_id != 0:
        c.delete(walls[wallCounter].line_id)
    walls[wallCounter].line_id = c.create_line(walls[wallCounter].x_start, walls[wallCounter].y_start, event.x, event.y)


def rightReleased(event):
    global wallCounter
    walls[wallCounter].x_end = event.x
    walls[wallCounter].y_end = event.y
    wallCounter += 1


def leftPressed(event):
    if not moveOnGoing:
        # minus 10 because of 20 radius of ball
        moveBallToNewPoint((event.x-10, event.y-10))


def moveBallToNewPoint(newCoords):
    global moveOnGoing
    moveOnGoing = True
    currentCoords = c.coords(ball)
    currentNp = np.array([currentCoords[0], currentCoords[1]])
    targetNp = np.array([newCoords[0], newCoords[1]])

    direction = np.subtract(targetNp, currentNp)

    magnitude = np.linalg.norm(direction)
    # normalize result vector to magnitude of 1
    normalizedDirection = []
    for comp in direction:
        normalizedDirection.append(comp / magnitude)

    # do the actual move
    c.move(ball, normalizedDirection[0], normalizedDirection[1])

    new_x = currentNp[0] + normalizedDirection[0]
    new_y = currentNp[1] + normalizedDirection[1]

    # if we are closer than 0.5 pixels, just move to the target
    if abs(new_x - targetNp[0]) < 1:
        c.coords(ball, (targetNp[0], new_y, targetNp[0]+20, new_y+20))
        new_x = targetNp[0]

    if abs(new_y - targetNp[1]) < 1:
        c.coords(ball, (new_x, targetNp[1], new_x+20, targetNp[1]+20))
        new_y = targetNp[1]

    if (new_x, new_y) != (targetNp[0], targetNp[1]):
        c.after(4, moveBallToNewPoint, targetNp)
    else:
        moveOnGoing = False


window.bind("<Button-3>", rightPressed)
window.bind("<B3-Motion>", rightMoved)
window.bind("<ButtonRelease-3>", rightReleased)
window.bind("<Button-1>", leftPressed)

c = Canvas(window, width=WIDTH, height=HEIGHT)
c.configure(background="#0a6c03")

ball = c.create_oval(40, 40, 60, 60, outline="#000", fill="#fff", width=2)

c.pack()
window.mainloop()
