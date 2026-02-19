import pygame
import sys
import math

pygame.init()

# Screen setup
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Car Movement")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()
FPS = 60

# Car properties
car_width = 100
car_height = 40
xl = (SCREEN_WIDTH // 2) - (car_width // 2)  # top-left x to center car
yl = (SCREEN_HEIGHT // 2) - (car_height // 2) # top-left y to center car
angle = 0           # facing angle in degrees
speed = 0           # current forward velocity
max_speed = 7
acceleration = 0.3
friction = 0.19
rotation_speed = 5  # degrees per frame

# Walls
wall_thickness = 20
wall_height = 300
left_wall_y = 300 
right_wall_x = 1420

right_wall_y = left_wall_y

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Rotate car
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        angle += rotation_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        angle -= rotation_speed

    # Accelerate forward/backward
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        speed += acceleration
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        speed -= acceleration
    else:
        # Apply friction
        if speed > 0:
            speed -= friction
            if speed < 0:
                speed = 0
        elif speed < 0:
            speed += friction
            if speed > 0:
                speed = 0

    # Clamp speed
    if speed > max_speed:
        speed = max_speed
    if speed < -max_speed / 2:
        speed = -max_speed / 2

    # Move in the direction the car is facing
    rad = math.radians(angle)
    xl += speed * math.cos(rad)
    yl -= speed * math.sin(rad)

    # Screen edge colliders
    if xl < 0:
        xl = 0
        speed = 0
    if xl + car_width > SCREEN_WIDTH:
        xl = SCREEN_WIDTH - car_width
        speed = 0
    if yl < 0:
        yl = 0
        speed = 0
    if yl + car_height > SCREEN_HEIGHT:
        yl = SCREEN_HEIGHT - car_height
        speed = 0

    # Drawing
    screen.fill(BLACK)

    # Draw rotating car
    car_surf = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
    car_surf.fill(WHITE)
    rotated_car = pygame.transform.rotate(car_surf, angle)
    rotated_rect = rotated_car.get_rect(center=(xl + car_width / 2, yl + car_height / 2))
    screen.blit(rotated_car, rotated_rect)

    # Draw walls
    pygame.draw.rect(screen, BLUE, (0, left_wall_y, wall_thickness, wall_height))
    pygame.draw.rect(screen, RED, (right_wall_x, right_wall_y, wall_thickness, wall_height))

    pygame.display.flip()
