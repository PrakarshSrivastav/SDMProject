import pygame
import sys

class GameOverService:
    def __init__(self, max_misses=3):
        """
        Initializes the GameOverService with a specified maximum number of missed objects.
        
        :param max_misses: The number of missed objects after which the game ends.
        """
        self.max_misses = max_misses
        self.missed_count = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 74)
        self.white_color = (255, 255, 255)

    def register_missed_object(self):
        """
        Increments the missed count. Ends the game if missed count reaches the max_misses.
        """
        if not self.game_over:
            self.missed_count += 1
            if self.missed_count >= self.max_misses:
                self.end_game()

    def end_game(self):
        """
        Ends the game by setting the game_over flag to True.
        """
        self.game_over = True

    def reset_game(self):
        """
        Resets the missed count and game_over flag to restart the game.
        """
        self.missed_count = 0
        self.game_over = False

    def is_game_over(self):
        """
        Returns whether the game is currently over.
        
        :return: True if the game is over, False otherwise.
        """
        return self.game_over

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

    def show_game_over_screen(self, screen):
        """
        Displays the "Game Over" screen on the provided surface.
        
        :param screen: The Pygame screen where the Game Over message is displayed.
        """
        game_over_text = self.font.render("Game Over", True, self.white_color)
        restart_text = self.font.render("Press R to Restart", True, self.white_color)
        quit_text = self.font.render("Press Q to Quit", True, self.white_color)
        

        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 3))
        screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() // 3 + 80))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, screen.get_height() // 3 + 160))