import unittest
from unittest.mock import Mock
import pygame
import sys
from game_over_service import GameOverService

class TestGameOverService(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        self.game_over_service = GameOverService(max_misses=3)
        self.screen_height = 600
        self.mock_screen = Mock()
        self.mock_event = Mock()
    
    def test_register_missed_object(self):
        self.game_over_service.register_missed_object()
        self.assertEqual(self.game_over_service.missed_count, 1)
        self.assertFalse(self.game_over_service.game_over)
        
        for _ in range(2):
            self.game_over_service.register_missed_object()
        self.assertTrue(self.game_over_service.game_over)

    def test_end_game(self):
        self.game_over_service.end_game()
        self.assertTrue(self.game_over_service.game_over)

    def test_reset_game(self):
        self.game_over_service.register_missed_object()
        self.game_over_service.reset_game()
        self.assertEqual(self.game_over_service.missed_count, 0)
        self.assertFalse(self.game_over_service.game_over)

    def test_is_game_over(self):
        self.assertFalse(self.game_over_service.is_game_over())
        self.game_over_service.end_game()
        self.assertTrue(self.game_over_service.is_game_over())

    def test_check_object_missed(self):
        object_rect = Mock()
        object_rect.top = self.screen_height + 1

        result = self.game_over_service.check_object_missed(object_rect, self.screen_height)
        self.assertTrue(result)
        self.assertEqual(self.game_over_service.missed_count, 1)

        object_rect.top = self.screen_height - 1
        result = self.game_over_service.check_object_missed(object_rect, self.screen_height)
        self.assertFalse(result)
        self.assertEqual(self.game_over_service.missed_count, 1)

    def test_handle_restart_or_quit_event_restart(self):
        self.game_over_service.end_game()
        self.mock_event.type = pygame.KEYDOWN
        self.mock_event.key = pygame.K_r
        self.game_over_service.handle_restart_or_quit_event(self.mock_event)
        self.assertFalse(self.game_over_service.game_over)
        self.assertEqual(self.game_over_service.missed_count, 0)

    def test_handle_restart_or_quit_event_quit(self):
        self.game_over_service.end_game()
        self.mock_event.type = pygame.KEYDOWN
        self.mock_event.key = pygame.K_q
        with self.assertRaises(SystemExit):
            self.game_over_service.handle_restart_or_quit_event(self.mock_event)

    def test_show_game_over_screen(self):
        self.mock_screen.get_width.return_value = 800
        self.mock_screen.get_height.return_value = 600
        self.game_over_service.show_game_over_screen(self.mock_screen)
        self.mock_screen.blit.assert_called()

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()