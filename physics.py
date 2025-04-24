import math
import pymunk
import pymunk.pygame_util
import pygame
class physics:
    def aoa(body):
        angle1 = body.angle
        velocity = body.velocity
        angle2 = math.atan2(velocity.y, velocity.x)
        # Angle of velocity vector
        aoa = angle1 - angle2
        return aoa
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