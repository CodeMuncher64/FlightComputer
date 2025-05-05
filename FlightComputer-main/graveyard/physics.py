import math
import pymunk
import pymunk.pygame_util
import pygame

def aoa(body):
    v1 = body.rotation_vector
    v2 = body.velocity.normalized()
    if v1.y <= v2.y:
        angle = math.acos(v1.dot(v2))
    else:
        angle = math.acos(v1.dot(v2)) * -1
    return angle
def lift(velocity, angle, x0=1):
    # Convert angle to radians
    # Calculate lift force
    if -1.5 < angle < 1.8:
        cof = 3.0*angle + 1 + -(angle**3)
    else: 
        cof = 0.0  
    lift_force = velocity.length * cof * x0

    return lift_force
def drag(velocity, angle, x0=1):
    vector = -(velocity**2) * math.sin(angle) * x0
    return vector