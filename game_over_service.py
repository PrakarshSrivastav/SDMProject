import pygame

class GameOverService:
    def __init__(self, max_misses=3):
        """
        Initializes the GameOverService with a specified maximum number of missed objects.
        
        :param max_misses: The number of missed objects after which the game ends.
        """
        self.max_misses = max_misses
        self.missed_count = 0
        self.game_over = False

    def register_missed_object(self):
        """
        Increments the missed count. Ends the game if missed count reaches the max_misses.
        """
        if not self.game_over:
            self.missed_count += 1
            print(f"Missed objects: {self.missed_count}/{self.max_misses}")
            if self.missed_count >= self.max_misses:
                self.end_game()

    def end_game(self):
        """
        Ends the game by setting the game_over flag to True.
        """
        self.game_over = True
        print("Game Over")

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