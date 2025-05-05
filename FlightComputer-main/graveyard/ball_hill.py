import pygame
import pymunk
import pymunk.pygame_util
import sys
import math

# Initialize pygame and pymunk
def draw_plane(screen, body, player_img):
    x, y = body.position
    angle = body.angle

    # Convert pymunk coordinates to pygame (Y is usually flipped)
    # assuming 600 is your screen height

    # Rotate the image based on the body's angle
    rotated_image = pygame.transform.rotate(player_img, -angle * 57.2958)  # radians to degrees
    rotated_rect = rotated_image.get_rect(center=(x, y))
    screen.blit(rotated_image, rotated_rect.topleft)
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Set up physics space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity pulls down

# Create the hill (static segment)
hill_body = pymunk.Body(body_type=pymunk.Body.STATIC)
hill_shape = pymunk.Segment(hill_body, (100, 300), (700, 500), 5)
hill_shape.friction = 0.9
space.add(hill_body, hill_shape)

# Create a ball
ball_body = pymunk.Body(mass=1, moment=10)
ball_body.position = (150, 150)
ball_shape = pymunk.Circle(ball_body, radius=20)
ball_shape.friction = 0.9
space.add(ball_body, ball_shape)
# load image
player_img = pygame.image.load("Daco_6091456.png").convert_alpha()
player_img = pygame.transform.flip(player_img, True, False)
player_img = pygame.transform.scale(player_img, (100, 50))  # Scale the image to fit the ball

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    print(ball_body.rotation_vector)
    screen.fill((255, 255, 255))  # Clear screen with white
    space.step(1/60.0)  # Step the physics simulation
    space.debug_draw(draw_options)  # Draw objects
    draw_plane(screen, ball_body, player_img)  # Draw the plane
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()