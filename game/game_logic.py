import pygame
from game.constants import *
from game.game_state import GameState
from game.player import Player
from game.square import Square
from services.game_over_services import GameOverService


class Game:
    def __init__(self, screen, clock, username, score_font):
        self.screen = screen
        self.clock = clock
        self.username = username
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
                             SCREEN_HEIGHT - PLAYER_HEIGHT - 10,
                             'assets/player/player.png'
        )
        self.squares = []
        self.collision_counter = 0
        self.spawn_counter = 0
        self.game_over_services = GameOverService(MAX_MISSES, username)
        self.heart_image = self.load_heart_image()
        self.sounds = self.load_sounds()
        self.game_over_sound_played = False
        self.score_font = score_font

        # Load background image
        self.background_image = pygame.image.load('assets/BG.jpg')  # replace with actual path
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_heart_image(self):
        try:
            heart_image = pygame.image.load('assets/heart.png')
            return pygame.transform.scale(heart_image, (30, 30))
        except Exception as e:
            print(f"Error loading heart image: {e}")
            return None

    def load_sounds(self):
        sounds = {}
        try:
            sounds['catch'] = pygame.mixer.Sound('assets/sounds/catch_object.wav')
            sounds['miss'] = pygame.mixer.Sound('assets/sounds/missed_object.wav')
            sounds['game_over'] = pygame.mixer.Sound('assets/sounds/game_over_sound.wav')
            sounds['background'] = pygame.mixer.Sound('assets/sounds/game_background.wav')

            # Adjust volumes
            sounds['catch'].set_volume(0.8)
            sounds['miss'].set_volume(0.8)
            sounds['game_over'].set_volume(0.8)
            sounds['background'].set_volume(0.2)

            # Play background music
            pygame.mixer.music.load('assets/sounds/game_background.wav')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1, 0.0)
        except Exception as e:
            print(f"Error loading sound: {e}")
            return {}
        return sounds

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def spawn_square(self):
        current_level = self.get_current_level()
        self.squares.append(Square(current_level))

    def get_current_level(self):
        if self.collision_counter < LEVEL_1_THRESHOLD:
            return 1
        elif self.collision_counter < LEVEL_2_THRESHOLD:
            return 2
        else:
            return 3

    def handle_collision(self, square):
        self.squares.remove(square)
        self.collision_counter += 1
        self.game_over_services.player_score = self.collision_counter
        self.play_sound('catch')

    def draw_game_state(self):

        self.screen.blit(self.background_image, (0, 0))

        if self.heart_image:
            for i in range(self.game_over_services.max_misses - self.game_over_services.missed_count):
                self.screen.blit(self.heart_image, (SCREEN_WIDTH - (i + 1)*50, 10))

        if not self.game_over_services.game_over:
            score_text = self.score_font.render(f"Score: {self.collision_counter}", True, BLACK)
            level_text = self.score_font.render(f"Level: {self.get_current_level()}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 50))

        self.player.draw(self.screen)
        for square in self.squares:
            square.draw(self.screen)

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        self.spawn_counter += 1
        if self.spawn_counter >= SPAWN_RATE:
            self.spawn_square()
            self.spawn_counter = 0

        for square in self.squares[:]:
            square.move()
            if square.is_off_screen():
                self.squares.remove(square)
                missed = self.game_over_services.check_object_missed(
                    pygame.Rect(square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), SCREEN_HEIGHT)
                if missed:
                    self.play_sound('miss')
            elif square.has_collided_with_player(self.player.rect):
                self.handle_collision(square)

        if self.game_over_services.is_game_over():
            if not self.game_over_sound_played:
                self.play_sound('game_over')
                self.game_over_sound_played = True
            self.squares.clear()

            return GameState.GAME_OVER

        return GameState.GAME
