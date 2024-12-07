import pygame
from leaderboard_service import LeaderboardService
from constants import *
from utils import Button
import sys
from game_state import GameState

def main_menu(screen, clock, font, game_over=False):
    button_width = 250
    button_height = 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 2 - (button_height + button_spacing)

    # Load the background image
    try:
        background_image = pygame.image.load('assets/BG.jpg')
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background_image = None

    main_button_text = "Restart" if game_over else "Start Game"
    main_button = Button(
        main_button_text,
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y,
        button_width,
        button_height,
        WHITE,
        GREY,
        font
    )

    leaderboard_button = Button(
        "Show Leaderboard",
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y + button_height + button_spacing,
        button_width,
        button_height,
        WHITE,
        GREY,
        font
    )

    quit_button = Button(
        "Quit",
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y + 2 * (button_height + button_spacing),
        button_width,
        button_height,
        WHITE,
        GREY,
        font
    )

    buttons = [main_button, leaderboard_button, quit_button]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background image
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)  # Fallback if the background image is missing

        for button in buttons:
            button.draw(screen, mouse_pos)
            if button.is_clicked(mouse_pos, mouse_pressed):
                if button.text == "Start Game" or button.text == "Restart":
                    return GameState.GAME
                elif button.text == "Show Leaderboard":
                    return GameState.LEADERBOARD
                elif button.text == "Quit":
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


def show_leaderboard(screen, clock, font, username):
    back_button = Button(
        "Back to Menu",
        50,
        SCREEN_HEIGHT - 100,
        150,
        50,
        WHITE,
        GREY,
        font
    )

    # Load the background image
    try:
        background_image = pygame.image.load('assets/Box.jpg')
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background_image = None

    leaderboard_service = LeaderboardService()
    top_scores = leaderboard_service.get_top_scores()
    user_scores = leaderboard_service.get_user_high_scores(username)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background image
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)  # Fallback if the background image is missing

        title_surf = font.render("Leaderboard - Top 10 Scores", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 4, 50))
        screen.blit(title_surf, title_rect)

        for idx, (uname, score) in enumerate(top_scores, start=1):
            score_text = f"{idx}. {uname} - {score}"
            score_surf = font.render(score_text, True, WHITE)
            score_rect = score_surf.get_rect(topleft=(50, 100 + idx * 30))
            screen.blit(score_surf, score_rect)

        user_title_surf = font.render("Your High Scores", True, WHITE)
        user_title_rect = user_title_surf.get_rect(center=(3 * SCREEN_WIDTH // 4, 50))
        screen.blit(user_title_surf, user_title_rect)

        for idx, score in enumerate(user_scores[:10], start=1):
            user_score_text = f"{idx}. {score}"
            user_score_surf = font.render(user_score_text, True, WHITE)
            user_score_rect = user_score_surf.get_rect(topleft=(SCREEN_WIDTH // 2 + 50, 100 + idx * 30))
            screen.blit(user_score_surf, user_score_rect)

        back_button.draw(screen, mouse_pos)
        if back_button.is_clicked(mouse_pos, mouse_pressed):
            return

        pygame.display.flip()
        clock.tick(FPS)
