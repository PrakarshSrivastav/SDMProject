import pygame

from services.main_menu import main_menu, show_leaderboard, pause_menu
from services.get_username import get_username
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.game_logic import Game
from game.game_state import GameState


def main():
    pygame.init()
    score_font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Catching Falling Objects')
    clock = pygame.time.Clock()

    username = get_username(screen, clock)
    state = GameState.MAIN_MENU
    game = Game(screen, clock, username, score_font)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and state == GameState.GAME:
                if event.key == pygame.K_p:  # Press 'P' to pause
                    state = GameState.PAUSE

        if state == GameState.MAIN_MENU:
            state = main_menu(screen, clock, pygame.font.Font(None, 36), game_over)
        elif state == GameState.LEADERBOARD:
            show_leaderboard(screen, clock, pygame.font.Font(None, 36), username)
            state = GameState.MAIN_MENU
            game = Game(screen, clock, username, score_font)
        elif state == GameState.GAME:
            state = game.update_game_state()
            game.draw_game_state()
            pygame.display.flip()
            clock.tick(FPS)
        elif state == GameState.GAME_OVER:
            game_over = True
            show_leaderboard(screen, clock, pygame.font.Font(None, 36), username)
            state = GameState.MAIN_MENU
            game = Game(screen, clock, username, score_font)
        elif state == GameState.PAUSE:
            state = pause_menu(screen, clock, pygame.font.Font(None, 36))


if __name__ == '__main__':
    main()