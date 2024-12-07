import pygame

from services.main_menu import main_menu, show_leaderboard
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if state == GameState.MAIN_MENU:
            state = main_menu(screen, clock, pygame.font.Font(None, 36))
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
            show_leaderboard(screen, clock, pygame.font.Font(None, 36), username)
            state = GameState.MAIN_MENU
            game = Game(screen, clock, username, score_font)


if __name__ == '__main__':
    main()