from tkinter import *
import numpy as np
from wall import Wall
from ball import Ball

HEIGHT = 900
WIDTH = 600

window = Tk()
window.title("Python Billiard")
window.resizable(False, False)

moveOnGoing = False
wallCounter = 0
walls = []

# init walls around window
# upperWall = Wall()
# upperWall.start = (0, 0)
# upperWall.end = (WIDTH, 0)
# walls.append(upperWall)
# wallCounter += 1
#
# rightWall = Wall()
# rightWall.start = (WIDTH, 0)
# rightWall.end = (WIDTH, HEIGHT)
# walls.append(rightWall)
# wallCounter += 1
#
# lowerWall = Wall()
# lowerWall.start = (0, HEIGHT)
# lowerWall.end = (WIDTH, HEIGHT)
# walls.append(lowerWall)
# wallCounter += 1
#
# leftWall = Wall()
# leftWall.start = (0, 0)
# leftWall.end = (0, HEIGHT)
# walls.append(leftWall)
# wallCounter += 1

def rightPressed(event):
    walls.append(Wall())
    walls[wallCounter].start = (event.x, event.y)


def rightMoved(event):
    if walls[wallCounter].line_id != 0:
        c.delete(walls[wallCounter].line_id)
    walls[wallCounter].line_id = c.create_line(walls[wallCounter].start[0], walls[wallCounter].start[1], event.x, event.y)


def rightReleased(event):
    global wallCounter
    walls[wallCounter].end = (event.x, event.y)
    walls[wallCounter].calc_vector()
    wallCounter += 1


def leftPressed(event):
    current = ball.pos
    target = np.array([event.x, event.y])
    direction_v = np.subtract(target, current)

    for w in walls:
        # calculate intersection point
        x_coord = np.array([direction_v[0], -1 * w.vector[0]])
        y_coord = np.array([direction_v[1], -1 * w.vector[1]])

        variables = np.stack((x_coord, y_coord), axis=0)
        absolute = np.array([w.start[0] - current[0], w.start[1] - current[1]])
        var_t = np.linalg.solve(variables, absolute)[0]

        intersect = np.array([current[0] + var_t * direction_v[0],
                              current[1] + var_t * direction_v[1]])
        moveBallToNewPoint((intersect[0], intersect[1]))


def moveBallToNewPoint(newCoords):
    global moveOnGoing
    moveOnGoing = True
    current = ball.pos
    target = np.array([newCoords[0], newCoords[1]])

    direction_v = np.subtract(target, current)

    magnitude = np.linalg.norm(direction_v)
    # normalize result vector to magnitude of 1
    normalizedDirection = []
    for comp in direction_v:
        normalizedDirection.append(comp / magnitude)

    # do the actual move
    ball.move(normalizedDirection[0], normalizedDirection[1])

    # if we are closer than 1 pixel, just move to the target (on the X or Y axis)
    if abs(ball.pos[0] - target[0]) < 1:
        ball.moveTo((target[0], ball.pos[1])) # move to X-target
    if abs(ball.pos[1] - target[1]) < 1:
        ball.moveTo((ball.pos[0], target[1])) # move to Y-target

    # if the final destination has not yet been reached, call move method again
    if (ball.pos[0], ball.pos[1]) != (target[0], target[1]):
        c.after(4, moveBallToNewPoint, target)
    else:
        moveOnGoing = False # we are finished with the move


window.bind("<Button-3>", rightPressed)
window.bind("<B3-Motion>", rightMoved)
window.bind("<ButtonRelease-3>", rightReleased)
window.bind("<Button-1>", leftPressed)

c = Canvas(window, width=WIDTH, height=HEIGHT)
c.configure(background="#0a6c03")

ball = Ball(c)
ball.draw()

c.pack()
window.mainloop()
