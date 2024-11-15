import pygame
import sys
from leaderboard_service import LeaderboardService

class GameOverService:
    def __init__(self, max_misses=3, username: str = "Player"):
        """
        Initializes the GameOverService with a specified maximum number of missed objects.

        :param max_misses: The number of missed objects after which the game ends.
        :param username: The username of the current player.
        """
        self.max_misses = max_misses
        self.missed_count = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.white_color = (255, 255, 255)
        self.leaderboard_service = LeaderboardService()
        self.username = username
        self.player_score = 0
        self.score_saved = False

    def register_missed_object(self):
        """
        Increments the missed count. Ends the game if missed count reaches the max_misses.
        """
        if not self.game_over:
            self.missed_count += 1
            if self.missed_count >= self.max_misses:
                self.end_game(self.player_score)

    def end_game(self, final_score):
        """
        Ends the game by setting the game_over flag to True and saving the player's score.

        :param final_score: The player's final score to be saved.
        """
        self.game_over = True
        self.player_score = final_score
        print(f"Saving score: {self.username} - {self.player_score}")
        try:
            self.leaderboard_service.save_score(self.username, self.player_score)
            self.score_saved = True
            print("Score saved successfully.")
        except Exception as e:
            print(f"Error saving score: {e}")

        self.top_scores = self.leaderboard_service.get_top_scores()
        self.user_scores = self.leaderboard_service.get_user_high_scores(self.username)

    def reset_game(self):
        """
        Resets the missed count and game_over flag to restart the game.
        """
        self.missed_count = 0
        self.game_over = False
        self.player_score = 0
        self.score_saved = False

    def is_game_over(self):
        """
        Returns whether the game is currently over.

        :return: True if the game is over, False otherwise.
        """
        return self.game_over

    def handle_restart_or_quit_event(self, event):
        """
        Handles the restart or quit event if the game is over. Resets the game if 'R' is pressed,
        or quits the game if 'Q' is pressed.

        :param event: The pygame event to check.
        """
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    def check_object_missed(self, object_rect, screen_height):
        """
        Checks if an object has fallen past the bottom of the screen. If so, registers it as missed.

        :param object_rect: The pygame.Rect representing the object's position and size.
        :param screen_height: The height of the game screen.
        """
        if object_rect.top > screen_height:
            self.register_missed_object()
            return True
        return False