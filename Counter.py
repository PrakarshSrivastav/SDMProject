import pygame
import sys
import random


pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Cube with Counter")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Cube properties
cube_width, cube_height = 30, 30  # Smaller size for the cube
cube_x = (width - cube_width) // 2  # Centered horizontally
cube_y = height - cube_height - 10  # Placed at the bottom with a 10-pixel margin
cube_speed = 5

# Falling object properties
falling_width, falling_height = 30, 30
falling_x = random.randint(0, width - falling_width)
falling_y = -falling_height  # Start above the screen
falling_speed = 5

# Counter
collision_count = 0
font = pygame.font.Font(None, 36)  # Font for displaying the counter

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move cube left and right
    if keys[pygame.K_LEFT] and cube_x > 0:
        cube_x -= cube_speed
    if keys[pygame.K_RIGHT] and cube_x < width - cube_width:
        cube_x += cube_speed

    # Move falling object
    falling_y += falling_speed

    # Reset falling object if it goes off the screen
    if falling_y > height:
        falling_y = -falling_height
        falling_x = random.randint(0, width - falling_width)

    # Check for collision
    cube_rect = pygame.Rect(cube_x, cube_y, cube_width, cube_height)
    falling_rect = pygame.Rect(falling_x, falling_y, falling_width, falling_height)
    if cube_rect.colliderect(falling_rect):
        collision_count += 1
        # Reset falling object after collision
        falling_y = -falling_height
        falling_x = random.randint(0, width - falling_width)

    # Fill the screen with white
    window.fill(white)
    
    # Draw the cube
    pygame.draw.rect(window, black, (cube_x, cube_y, cube_width, cube_height))
    
    # Draw the falling object
    pygame.draw.rect(window, red, (falling_x, falling_y, falling_width, falling_height))
    
    # Render and display the counter
    counter_text = font.render(f"Collisions: {collision_count}", True, black)
    window.blit(counter_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
sys.exit()
