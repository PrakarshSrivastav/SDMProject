import pygame
import random
import sys
from constants import *

pygame.init()
SCORE_FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Squares")
clock = pygame.time.Clock()

class Square:
    #added in Sprint 2
    images = [
        pygame.transform.scale(
            pygame.image.load(f'assets/obj{i}.png'),
            (SQUARE_SIZE * 1, SQUARE_SIZE *1)  # Adjust the multiplier to make them larger
        ) for i in range(1, 17)
    ]
    
    def __init__(self):
        self.image = random.choice(Square.images)  # Randomly choose an image
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()  # Start above the screen
        self.speed = FALL_SPEED
        
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
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
