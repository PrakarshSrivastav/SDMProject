import pygame
import random
import sys

from game_over_services import GameOverService

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
MAX_MISSES = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Different colors for squares
SCORE_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching Falling Objects")
clock = pygame.time.Clock()

player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH,
                          PLAYER_HEIGHT)

catch_sound = pygame.mixer.Sound('sounds/catch_object.wav')
miss_sound = pygame.mixer.Sound('sounds/missed_object.wav')
game_over_sound = pygame.mixer.Sound('sounds/game_over_sound.wav')
game_background_sound = pygame.mixer.Sound('sounds/game_background.wav')

catch_sound.set_volume(0.8)
miss_sound.set_volume(0.8)
game_over_sound.set_volume(0.8)
game_background_sound.set_volume(0.2)

pygame.mixer.music.load('sounds/game_background.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 30
SPAWN_RATE = 100
FALL_SPEED = 3
FPS = 60
MAX_MISSES = 3

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Squares")
clock = pygame.time.Clock()

def main():
    squares = []
    spawn_counter = 0
    collision_counter = 0
    running = True
    game_over_services = GameOverService(MAX_MISSES)
    game_over_sound_played = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            game_over_services.handle_restart_or_quit_event(event)

        if not game_over_services.is_game_over():
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
                if square.is_off_screen() and game_over_services.check_object_missed(pygame.Rect(square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), SCREEN_HEIGHT):
                    squares.remove(square)
                    miss_sound.play()
                elif square.has_collided_with_player(player_rect):
                    squares.remove(square)
                    collision_counter += 1
                    catch_sound.play()

        screen.fill(BLACK)

        if game_over_services.is_game_over():
            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            game_over_services.show_game_over_screen(screen)
            squares.clear()
            collision_counter = 0
        else:
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
