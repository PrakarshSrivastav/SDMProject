import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 30
SPAWN_RATE = 100  # Frames between spawns
FALL_SPEED = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Different colors for squares

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Squares")
clock = pygame.time.Clock()

class Square:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - SQUARE_SIZE)
        self.y = -SQUARE_SIZE  # Start above the screen
        self.color = random.choice(COLORS)
        self.speed = FALL_SPEED
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

def main():
    try:
        squares = []
        spawn_counter = 0
        running = True

        # Main game loop
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Spawn new squares
            spawn_counter += 1
            if spawn_counter >= SPAWN_RATE:
                squares.append(Square())
                spawn_counter = 0

            # Update squares
            for square in squares[:]:
                square.move()
                if square.is_off_screen():
                    squares.remove(square)

            # Drawing
            screen.fill(BLACK)
            for square in squares:
                square.draw(screen)
            
            # Update the display
            pygame.display.flip()

            # Control game speed
            clock.tick(FPS)

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()