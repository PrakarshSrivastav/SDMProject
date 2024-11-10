import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
MOVE_SPEED = 10
SQUARE_SIZE = 30
SPAWN_RATE = 100  # Frames between spawns
FALL_SPEED = 3
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Different colors for squares
SCORE_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching Falling Objects")
clock = pygame.time.Clock()

player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH,
                          PLAYER_HEIGHT)


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

    def has_collided_with_player(self, player):
        square_rect = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)
        return square_rect.colliderect(player)


def main():
    squares = []
    spawn_counter = 0
    collision_counter = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += MOVE_SPEED

        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH

        spawn_counter += 1
        if spawn_counter >= SPAWN_RATE:
            squares.append(Square())
            spawn_counter = 0

        for square in squares[:]:
            square.move()
            if square.is_off_screen():
                squares.remove(square)
            elif square.has_collided_with_player(player_rect):
                squares.remove(square)
                collision_counter += 1

        screen.fill(BLACK)
        for square in squares:
            square.draw(screen)

        pygame.draw.rect(screen, WHITE, player_rect)
        counter_text = SCORE_FONT.render(f"Collision Counter: {collision_counter}", True, WHITE)
        screen.blit(counter_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
