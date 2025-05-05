import pygame
import pymunk
import pymunk.pygame_util
import math
from pymunk.vec2d import Vec2d
# from physics import physics


def create_car(space, position=(100, 100)):
    # === Car Body ===
    # chassis_size = (60, 30)
    # chassis_moment = pymunk.moment_for_box(chassis_mass, chassis_size)
    chassis_body = pymunk.Body()
    chassis_body.position = position
    chassis_shape = pymunk.Poly(chassis_body, [(-100,0), (100,10), (100, -10), (-100, -10)])
    chassis_shape.density = 0.05
    chassis_shape.elasticity = 1
    chassis_shape.friction = 0.7
    space.add(chassis_body, chassis_shape)

    # === Wheels ===

    
    l_offset_x = -60
    l_offset_y = 20
    r_offset_x = 60
    r_offset_y = 30

    # Left wheel
    left_wheel = pymunk.Body()
    left_wheel.position = chassis_body.position + Vec2d(l_offset_x, l_offset_y)
    left_shape = pymunk.Circle(left_wheel, 10)
    left_shape.friction = 1
    left_shape.elasticity = 0.4
    left_shape.density = 0.1

    # Right wheel
    right_wheel = pymunk.Body()
    right_wheel.position = chassis_body.position + Vec2d(r_offset_x, r_offset_y)
    right_shape = pymunk.Circle(right_wheel, 15)
    right_shape.friction = 1
    right_shape.elasticity = 0.4
    right_shape.density = 0.1

    space.add(left_wheel, left_shape, right_wheel, right_shape)

    # # === Joints ===
    left_joint = pymunk.PinJoint(chassis_body, left_wheel, (l_offset_x, l_offset_y))
    
    right_joint = pymunk.PinJoint(chassis_body, right_wheel, (r_offset_x, r_offset_y))
     # Optional: suspension springs
    # left_spring = pymunk.DampedSpring(chassis_body, left_wheel, (-offset_x, offset_y), (0, 0), 
    #                                     rest_length=1, stiffness=2000, damping=100)
    # right_spring = pymunk.DampedSpring(chassis_body, right_wheel, (offset_x, offset_y), (0, 0), 
    #                                     rest_length=1, stiffness=2000, damping=100)

    space.add(left_joint, right_joint)

    return chassis_body, left_wheel, right_wheel



def draw_plane(world, body, player_img):
    x, y = body.position
    angle = body.angle

    # Convert pymunk coordinates to pygame (Y is usually flipped)
    # assuming 600 is your screen height

    # Rotate the image based on the body's angle
    rotated_image = pygame.transform.rotate(player_img, -angle * 57.2958)  # radians to degrees
    rotated_rect = rotated_image.get_rect(center=(x, y))
    world.blit(rotated_image, rotated_rect.topleft)



def aoa(body):

    v1 = body.rotation_vector
    v2 = body.velocity.normalized()
    if v1.y <= v2.y:
        angle = math.acos(v1.dot(v2))
    else:
        angle = math.acos(v1.dot(v2)) * -1
    return angle



def lift(velocity, angle, x0=1):
    if -1.5 < angle < 1.8:
        cof = 3.0*angle + 1 - (angle**3)
    else: 
        cof = 0.0  
    lift_force = velocity.length * cof * x0
    return lift_force



def drag(velocity, angle, x0=1):
    return velocity.normalized() * -velocity.length**2 * (((2*math.sin(angle)))**2+4)* x0



def PID(error, tick = 60):
    # if len(error) < 3:
    #     return None, None, None
    P = error[-1] # degrees per second of error 
    I = sum(error)/tick # total degrees of error
    #D = (error[-1] - error[-2]) * tick # degrees per second of error
    D = (((sum(error[-5:]))-(sum(error[-10:-5]))*(tick))/5) # degrees per second per second of error  
    return P, I, D



def control(P, I, D, master = 1):
    # PID control
    Kp = 0.5
    Ki = 0.5
    Kd = 0.001 #DERIVATIVE TERM loves to spike so we need to dampen it
    # Calculate the control output
    control_output = (Kp * P + Ki * I + Kd * D)*master
    return control_output



def create_world(WINDOW_WIDTH = 1400, WINDOW_HEIGHT= 600, WORLD_WIDTH = 10000, WORLD_HEIGHT = 2000):
    # Initialize Pygame
    pygame.init()
    space = pymunk.Space()
    space.gravity = (0, 981)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("plane and PID Simulation")


    # creates a text box
    font = pygame.font.Font(None, 20)
    text_panel = pygame.Surface((WINDOW_WIDTH, 50))
    text_panel.fill((10, 10, 10))


    # Set up world
    world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT)) # Fill with a dark color
    grid = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    grid.fill((200, 200, 200))
    for i in range(0, WORLD_WIDTH, 50):
        pygame.draw.line(grid, (0,0,0), (i, 0), (i, WORLD_HEIGHT),5)
    for i in range(0, WORLD_HEIGHT, 50):
        pygame.draw.line(grid, (0,0,0), (0, i), (WORLD_WIDTH, i),5)
    world.blit(grid, (0, 0))
    draw_options = pymunk.pygame_util.DrawOptions(world)


    # Set up walls

    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor = pymunk.Segment(static_body, (0, WORLD_HEIGHT-10), (WORLD_WIDTH, WORLD_HEIGHT-10), 20)
    floor.elasticity = 0.1
    floor.friction = 0.8
    floor.density = 10
    space.add(static_body, floor)


    
    # Creates the players plane

    chassis, left_wheel, right_wheel = create_car(space, position=(200, WORLD_HEIGHT-150)) 

    # load player image
    player_img = pygame.image.load("Daco_6091456.png").convert_alpha()
    player_img = pygame.transform.flip(player_img, True, False)
    player_img = pygame.transform.rotate(player_img, 5)
    player_img = pygame.transform.scale(player_img, (300, 100))


    # seting up for PID 
    error = [0.0] * 60 #the game is 60 tick so this records one second of data
    control_mode = "manual"
    #control_mode = "PID"
    #control_mode = "pseudo_PID"
    rotation_control = 1 # how much the plane should rotate per second in radians used by the PID controller 
 
    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # teleports the plane to the other side of the screen if it reaches near the edge
        if chassis.position[0] > WORLD_WIDTH-2000:
            chassis.position = (1000, chassis.position[1])
            right_wheel.position = (chassis.position[0] + 60, chassis.position[1] + 30)
            left_wheel.position = (chassis.position[0] - 60, chassis.position[1] + 20)
            continue
        # calculates the aerodynamic forces on the aircraft
        angle = aoa(chassis)
        lift_force = lift(chassis.velocity, angle, 300)
        drag_force = drag(chassis.velocity, angle, 1/50)

        chassis.apply_force_at_local_point((0,-lift_force), (20,0))
        chassis.apply_force_at_local_point((drag_force), (0,0))

        # because of how the aero surfaces are set up the plane is very unstable and hard to fly
        # this is good because it allows us to demonstrate the PID controller
        # I will madde three control modes
        # 1. manual control (M)
        # manual control will use up and down forces at the back of the plane to control the pitch 
        # this is similar to the elevator on a real plane

        # 2. PID control (P)
        # PID control will use the same control surfaces as manual to control the plane but will use target rotation rates as input and
        # output a control command that will push the plane to best match the target rotation rate.  

        # 3. pseudo PID control (S)
        # The pseudo PID will use hard coded command of rotation rate to show what a perfect PID controller should look like
  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            chassis.apply_force_at_local_point((80000, 0))
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_p]:
            control_mode = "PID"
        if keys[pygame.K_m]:
            control_mode = "manual"
        if keys[pygame.K_s]:
            control_mode = "pseudo_PID"
    
        #manual control
        if control_mode == "manual":
            if keys[pygame.K_UP]:
                chassis.apply_force_at_local_point((0, chassis.velocity.length * 100),(-100,0))
            if keys[pygame.K_DOWN]:
                chassis.apply_force_at_local_point((0, -chassis.velocity.length * 100), (-100,0))
     
     
        #PID control 
        elif control_mode == "PID":
            # builds the target and observed values #radians per second
            if keys[pygame.K_UP]:
                target = -rotation_control
            elif keys[pygame.K_DOWN]:
                target = rotation_control
            else:
                target = 0
            error.append(chassis.angular_velocity - target)   
            error.pop(0)
            P, I, D = PID(error)
            control_output = control(P, I, D, 500)
            print(control_output)
            chassis.apply_force_at_local_point((0, chassis.velocity.length*control_output), (-100,0))
            # a negative force is an upward push at the back of the plane which will cause 
            # the plane to rotate down which is positive in pymunk
            # if the error is - it means the plane is rotating up and we need to push down
            # if the error is + it means the plane is rotating down and we need to push up

            
            
        #pseudo PID control
        elif control_mode == "pseudo_PID":
            if keys[pygame.K_UP]:
                chassis.angular_velocity = -rotation_control
            elif keys[pygame.K_DOWN]:
                chassis.angular_velocity = rotation_control
            else:
                chassis.angular_velocity = 0
                


        # Calculate camera (centered on player)
        body_pos = chassis.position
        camera_x = body_pos[0] - 300
        camera_y = body_pos[1] - WINDOW_HEIGHT // 2

        # Clamp camera to world bounds
        camera_x = max(0, min(WORLD_WIDTH - WINDOW_WIDTH, camera_x))
        camera_y = max(0, min(WORLD_HEIGHT - WINDOW_HEIGHT, camera_y))

        # Blit part of world to screen (camera view)
        world.blit(grid, (0, 0))
        space.debug_draw(draw_options)
        draw_plane(world, chassis, player_img)
        screen.blit(world, (0, 0), area=pygame.Rect(camera_x, camera_y, WINDOW_WIDTH, WINDOW_HEIGHT))

        # Draw the text panel
        text = font.render("Use UP and DOWN arrow to control the plane pitch: Use LEFT arrow for throttle: press M, P, or S to cycle through control modes. Current Mode: " + control_mode, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 25))
        text_panel.fill((10, 10, 10))
        text_panel.blit(text, text_rect)
        screen.blit(text_panel, (0, 0))

        pygame.display.flip()
        dt = clock.tick(60)
        # Update physics
        space.step(dt / 1000.0)

    pygame.quit()

if __name__ == "__main__":
    create_world(1400, 600, 10000, 2000)