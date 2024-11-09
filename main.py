import pygame
import random
import sys
from game_over_service import GameOverService

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 30
SPAWN_RATE = 100
FALL_SPEED = 3
FPS = 60
MAX_MISSES = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Squares")
clock = pygame.time.Clock()

class Square:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - SQUARE_SIZE)
        self.y = -SQUARE_SIZE
        self.color = random.choice(COLORS)
        self.speed = FALL_SPEED
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

def main():
    squares = []
    spawn_counter = 0
    running = True
    game_over_service = GameOverService(MAX_MISSES)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            game_over_service.handle_restart_or_quit_event(event)

        if not game_over_service.is_game_over():
            spawn_counter += 1
            if spawn_counter >= SPAWN_RATE:
                squares.append(Square())
                spawn_counter = 0

            for square in squares[:]:
                square.move()
                if game_over_service.check_object_missed(pygame.Rect(square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), SCREEN_HEIGHT):
                    squares.remove(square)
                elif square.is_off_screen():
                    squares.remove(square)

        screen.fill(BLACK)
        
        if game_over_service.is_game_over():
            game_over_service.show_game_over_screen(screen)
            squares.clear()
        else:
            for square in squares:
                square.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()