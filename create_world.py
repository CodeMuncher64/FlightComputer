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
    chassis_shape = pymunk.Poly(chassis_body, [(-60,0), (60,10), (60, -10), (-60, -10)])
    chassis_shape.density = 0.1
    chassis_shape.elasticity = 0.1
    chassis_shape.friction = 0.7
    space.add(chassis_body, chassis_shape)

    # === Wheels ===
    wheel_radius = 10

    
    l_offset_x = -40
    l_offset_y = 20
    r_offset_x = 40
    r_offset_y = 30

    # Left wheel
    left_wheel = pymunk.Body()
    left_wheel.position = chassis_body.position + Vec2d(l_offset_x, l_offset_y)
    left_shape = pymunk.Circle(left_wheel, wheel_radius)
    left_shape.friction = 1
    left_shape.elasticity = 0.4
    left_shape.density = 0.1

    # Right wheel
    right_wheel = pymunk.Body()
    right_wheel.position = chassis_body.position + Vec2d(r_offset_x, r_offset_y)
    right_shape = pymunk.Circle(right_wheel, wheel_radius)
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
def aoa(body):
    angle1 = body.angle
    velocity = body.velocity
    v1 = body.velocity.normalized()
    angle2 = math.atan2(v1.y, v1.x)
     # Angle of velocity vector
    return 1
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
    return velocity.normalized() * velocity.length**2 * (math.sin(angle)+1)* x0

def create_world(WINDOW_WIDTH = 800, WINDOW_HEIGHT= 600, WORLD_WIDTH = 10000, WORLD_HEIGHT = 2000):
    # Initialize Pygame
    pygame.init()
    space = pymunk.Space()
    space.gravity = (0, 981)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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
    # Set up player
    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor = pymunk.Segment(static_body, (0, WORLD_HEIGHT-10), (WORLD_WIDTH, WORLD_HEIGHT-10), 20)
    floor.elasticity = 0.1
    floor.friction = 0.8
    floor.density = 10
    space.add(static_body, floor)

    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    left_wall = pymunk.Segment(static_body, (0, 0), (0, WORLD_HEIGHT), 5)
    left_wall.elasticity = 0.4
    left_wall.friction = 0.8
    space.add(static_body, left_wall)

    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    right_wall = pymunk.Segment(static_body, (WORLD_WIDTH, 0), (WORLD_WIDTH, WORLD_HEIGHT), 5)
    right_wall.elasticity = 0.4
    right_wall.friction = 0.8

    
    # Create a player body

    chassis, left_wheel, right_wheel = create_car(space, position=(200, WORLD_HEIGHT-150)) 
    
    print(chassis.angle)
    print(math.sin(chassis.angle))
    print(math.cos(chassis.angle))

    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        #calculates airodynamic forces
        angle = aoa(chassis)
        lift_normal = pymunk.Vec2d(math.sin(chassis.angle), -math.cos(chassis.angle))
        # drag(body.velocity, angle)
        net_force = lift_normal*lift(chassis.velocity, angle,10)*10
        force = (net_force.x,net_force.y)
        chassis.apply_force_at_local_point(force)

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_UP]:
            chassis.apply_force_at_local_point((0, -4000),(50,0))
        if keys[pygame.K_RIGHT]:
            chassis.apply_force_at_local_point((40000, 0))


        #Clamp player to world
        # player_pos[0] = max(0, min(WORLD_WIDTH - player_size, player_pos[0]))
        # player_pos[1] = max(0, min(WORLD_HEIGHT - player_size, player_pos[1]))

        # Clear world

        # Draw pymunk to world

        # Calculate camera (centered on player)
        body_pos = chassis.position
        camera_x = body_pos[0] - WINDOW_WIDTH // 2
        camera_y = body_pos[1] - WINDOW_HEIGHT // 2
        # Clamp camera to world bounds
        camera_x = max(0, min(WORLD_WIDTH - WINDOW_WIDTH, camera_x))
        camera_y = max(0, min(WORLD_HEIGHT - WINDOW_HEIGHT, camera_y))

        # Blit part of world to screen (camera view)
        world.blit(grid, (0, 0))
        space.debug_draw(draw_options)
        screen.blit(world, (0, 0), area=pygame.Rect(camera_x, camera_y, WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.flip()
        dt = clock.tick(60)
        # Update physics
        space.step(dt / 1000.0)

    pygame.quit()

if __name__ == "__main__":
    create_world()