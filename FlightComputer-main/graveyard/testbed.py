import pygame
import pymunk
import pymunk.pygame_util
import math
def aoa(body):
    angle1 = body.angle
    velocity = body.velocity
    angle2 = math.atan2(velocity.y, velocity.x)
     # Angle of velocity vector
    aoa = angle1 - angle2
    return aoa


angle1 = math.pi/4
print(angle1)
velocity = (-1, 1)
angle2 = math.atan2(velocity[1], velocity[0])
print(angle2)
    # Angle of velocity vector
aoa = angle1 - angle2
print(aoa)