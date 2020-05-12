import time
from tkinter import *

import numpy as np
from wall import Wall
from ball import Ball

HEIGHT = 900
WIDTH = 600

window = Tk()
window.title("Python Billiard")
window.resizable(False, False)

move_completed = None
wallCounter = 0
walls = []

# init walls around window
upperWall = Wall()
upperWall.start = (0, 0)
upperWall.end = (WIDTH, 0)
upperWall.calc_vector()
walls.append(upperWall)
wallCounter += 1

rightWall = Wall()
rightWall.start = (WIDTH, 0)
rightWall.end = (WIDTH, HEIGHT)
rightWall.calc_vector()
walls.append(rightWall)
wallCounter += 1

lowerWall = Wall()
lowerWall.start = (0, HEIGHT)
lowerWall.end = (WIDTH, HEIGHT)
lowerWall.calc_vector()
walls.append(lowerWall)
wallCounter += 1

leftWall = Wall()
leftWall.start = (0, 0)
leftWall.end = (0, HEIGHT)
leftWall.calc_vector()
walls.append(leftWall)
wallCounter += 1


def rightPressed(event):
    walls.append(Wall())
    walls[wallCounter].start = (event.x, event.y)


def rightMoved(event):
    if walls[wallCounter].line_id != 0:
        c.delete(walls[wallCounter].line_id)
    walls[wallCounter].line_id = c.create_line(walls[wallCounter].start[0], walls[wallCounter].start[1], event.x,
                                               event.y)


def rightReleased(event):
    global wallCounter
    walls[wallCounter].end = (event.x, event.y)
    walls[wallCounter].calc_vector()
    wallCounter += 1


def leftPressed(event):
    current = ball.pos
    target = np.array([event.x, event.y])
    direction_v = np.subtract(target, current)
    calc_next_intersection(direction_v)


def calc_next_intersection(direction_v):
    for wall in walls:
        # calculate intersection point
        x_coord = np.array([direction_v[0], -1 * wall.vector[0]])
        y_coord = np.array([direction_v[1], -1 * wall.vector[1]])
        variables = np.stack((x_coord, y_coord), axis=0)

        absolute = np.array([wall.start[0] - ball.pos[0], wall.start[1] - ball.pos[1]])

        var_t = np.linalg.solve(variables, absolute)[0]
        wall.last_intersection_coefficient = var_t

    # sort by "t" variable, ascending
    walls.sort(key=lambda w: w.last_intersection_coefficient, reverse=False)

    # loop over the walls until:
    # a) the nearest wall has a positive intersection coefficient
    # b) where the intersection point of the nearest wall lies between start and end point!
    i = 0
    while True:
        nearest_wall = walls[i]
        intersection = np.array([ball.pos[0] + nearest_wall.last_intersection_coefficient * direction_v[0],
                                 ball.pos[1] + nearest_wall.last_intersection_coefficient * direction_v[1]])
        i += 1
        if nearest_wall.last_intersection_coefficient > 0 and nearest_wall.intersect_is_in_bounds(intersection):
            break

    # mirror the ball position on the wall he is going to hit
    mirror_point = mirror_current_ball_pos(nearest_wall)

    # perform animation
    move_ball_to_new_point(intersection[0], intersection[1])
    print("finished")


    # calculate the reflection direction
    reflection_direction = np.subtract(intersection, mirror_point)

    # recursive call to calculate the next intersection in the calculated reflection direction
    #calc_next_intersection(reflection_direction)


def move_ball_to_new_point(x_coord, y_coord):
    global move_completed
    move_completed = False
    current = ball.pos
    target = np.array([x_coord, y_coord])

    direction_v = np.subtract(target, current)
    magnitude = np.linalg.norm(direction_v)
    # normalize result vector to magnitude of 1
    normalized_direction = []
    for comp in direction_v:
        normalized_direction.append(comp / magnitude)

    # do the actual move
    ball.move(normalized_direction[0], normalized_direction[1])

    # if we are closer than 1 pixel, just move to the target (on the X or Y axis)
    if abs(ball.pos[0] - target[0]) < 1:
        ball.moveTo((target[0], ball.pos[1]))  # move to X-target
    if abs(ball.pos[1] - target[1]) < 1:
        ball.moveTo((ball.pos[0], target[1]))  # move to Y-target

    # if the final destination has been reached, set the global variable to false
    if (ball.pos[0], ball.pos[1]) != (target[0], target[1]):
        c.after(4, move_ball_to_new_point, target[0], target[1])
    else:
        print("finished!")
        move_completed = True


def mirror_current_ball_pos(nearest_wall):
    # calculate vector perpendicular to wall (perpendicular to (n1, n2) --> (n2, -n1))
    perpendicular_vector = np.array([nearest_wall.vector[1], -1 * nearest_wall.vector[0]])

    # calculate intersection between wall and line perpendicular to wall through current ball pos
    x_coord = np.array([perpendicular_vector[0], -1 * nearest_wall.vector[0]])
    y_coord = np.array([perpendicular_vector[1], -1 * nearest_wall.vector[1]])
    variables = np.stack((x_coord, y_coord), axis=0)

    absolute = np.array([nearest_wall.start[0] - ball.pos[0], nearest_wall.start[1] - ball.pos[1]])

    var_t = np.linalg.solve(variables, absolute)[0]
    intersection = np.array([ball.pos[0] + var_t * perpendicular_vector[0],
                             ball.pos[1] + var_t * perpendicular_vector[1]])

    # mirrored point is equal to current ball pos + 2 * the distance between the ball_pos and the intersection_point
    mirror_point = np.array([ball.pos[0] + 2 * (intersection[0] - ball.pos[0]),
                             ball.pos[1] + 2 * (intersection[1] - ball.pos[1])])
    return mirror_point


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
