import pygame
import random
import sys
from enum import Enum, auto
from game_over_services import GameOverService
from constants import *
from main_menu import main_menu, show_leaderboard
from game_state import GameState
from get_username import get_username

pygame.init()
SCORE_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching Falling Objects")
clock = pygame.time.Clock()

try:
    catch_sound = pygame.mixer.Sound('sounds/catch_object.wav')
    miss_sound = pygame.mixer.Sound('sounds/missed_object.wav')
    game_over_sound = pygame.mixer.Sound('sounds/game_over_sound.wav')
    game_background_sound = pygame.mixer.Sound('sounds/game_background.wav')
except pygame.error as e:
    pygame.quit()
    sys.exit()

catch_sound.set_volume(0.8)
miss_sound.set_volume(0.8)
game_over_sound.set_volume(0.8)
game_background_sound.set_volume(0.2)

try:
    pygame.mixer.music.load('sounds/game_background.wav')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0.0)
except pygame.error as e:
    print(f"Error loading background music: {e}")

player_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
    SCREEN_HEIGHT - PLAYER_HEIGHT - 10,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)

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
    try:
        current_username = get_username(screen, clock)
        print(f"Username: {current_username}")
        state = GameState.MAIN_MENU
        squares = []
        spawn_counter = 0
        collision_counter = 0
        game_over_services = GameOverService(MAX_MISSES, username=current_username)
        game_over_sound_played = False

        button_font = pygame.font.Font(None, 36)

        persistent_game_over = False

        while True:
            if not persistent_game_over:
                persistent_game_over = game_over_services.is_game_over()

            if state == GameState.MAIN_MENU:
                state = main_menu(screen, clock, button_font, game_over=persistent_game_over)
                if state == GameState.GAME:
                    persistent_game_over = False

            elif state == GameState.LEADERBOARD:
                show_leaderboard(screen, clock, button_font, current_username)
                state = GameState.MAIN_MENU

            elif state == GameState.GAME:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = GameState.MAIN_MENU

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
                        if square.is_off_screen():
                            squares.remove(square)
                            if game_over_services.check_object_missed(pygame.Rect(square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), SCREEN_HEIGHT):
                                miss_sound.play()
                        elif square.has_collided_with_player(player_rect):
                            squares.remove(square)
                            collision_counter += 1
                            game_over_services.player_score = collision_counter
                            catch_sound.play()

                screen.fill(BLACK)

                if game_over_services.is_game_over():
                    if not game_over_sound_played:
                        game_over_sound.play()
                        game_over_sound_played = True
                    squares.clear()
                    collision_counter = 0
                    state = GameState.GAME_OVER
                else:
                    for square in squares:
                        square.draw(screen)

                    pygame.draw.rect(screen, WHITE, player_rect)
                    counter_text = SCORE_FONT.render(f"Score: {collision_counter}", True, WHITE)
                    screen.blit(counter_text, (10, 10))

                pygame.display.flip()
                clock.tick(FPS)

            elif state == GameState.GAME_OVER:
                state = GameState.MAIN_MENU
                game_over_sound_played = False
                game_over_services.reset_game()
            else:
                state = GameState.MAIN_MENU
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
