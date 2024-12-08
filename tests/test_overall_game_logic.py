import unittest
from unittest.mock import Mock, patch
import pygame
from game.square import Square
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT

player_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
    SCREEN_HEIGHT - PLAYER_HEIGHT - 10,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """Setup required for the tests."""
        pygame.init()
        self.test_square = Square()

    def test_square_initial_position(self):
        """Test if the square is initialized above the screen."""
        self.assertLess(self.test_square.y, 0)
        self.assertGreaterEqual(self.test_square.x, 0)
        self.assertLess(self.test_square.x, SCREEN_WIDTH)

    def test_square_move(self):
        """Test if the square moves correctly."""
        initial_y = self.test_square.y
        self.test_square.move()
        self.assertEqual(self.test_square.y, initial_y + self.test_square.speed)

    def test_square_off_screen(self):
        """Test if is_off_screen correctly identifies when a square is off-screen."""
        self.test_square.y = SCREEN_HEIGHT + 1
        self.assertTrue(self.test_square.is_off_screen())

    def test_square_collision_with_player(self):
        """Test if has_collided_with_player detects collision with the player."""
        self.test_square.x = player_rect.x
        self.test_square.y = player_rect.y
        self.assertTrue(self.test_square.has_collided_with_player(player_rect))

    def test_square_no_collision_with_player(self):
        """Test if has_collided_with_player does not detect collision when not overlapping."""
        self.test_square.x = player_rect.x + 1000
        self.test_square.y = player_rect.y + 1000
        self.assertFalse(self.test_square.has_collided_with_player(player_rect))

    @patch('pygame.mixer.Sound')
    def test_sound_effects(self, mock_sound):
        """Test if sound effects play correctly."""
        catch_sound = Mock()
        miss_sound = Mock()

        self.test_square.x = player_rect.x
        self.test_square.y = player_rect.y
        if self.test_square.has_collided_with_player(player_rect):
            catch_sound.play()
            catch_sound.play.assert_called_once()

        self.test_square.y = SCREEN_HEIGHT + 1
        if self.test_square.is_off_screen():
            miss_sound.play()
            miss_sound.play.assert_called_once()


if __name__ == "__main__":
    unittest.main()
