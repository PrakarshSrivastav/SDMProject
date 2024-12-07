import unittest
from services.leaderboard_service import LeaderboardService


class TestLeaderboardService(unittest.TestCase):

    def setUp(self):
        """Set up an in-memory database for testing."""
        self.leaderboard_service = LeaderboardService(db_name=":memory:")
        self.leaderboard_service._initialize_database()

    def test_save_score(self):
        """Test saving a score."""
        self.leaderboard_service.save_score("Alice", 150)
        top_scores = self.leaderboard_service.get_top_scores()
        self.assertEqual(len(top_scores), 1)
        self.assertEqual(top_scores[0], ("Alice", 150))

    def test_get_top_scores(self):
        """Test retrieving top scores."""
        self.leaderboard_service.save_score("Alice", 150)
        self.leaderboard_service.save_score("Bob", 200)
        self.leaderboard_service.save_score("Alice", 180)
        top_scores = self.leaderboard_service.get_top_scores(limit=2)
        self.assertEqual(top_scores, [("Bob", 200), ("Alice", 180)])

    def test_get_user_high_scores(self):
        """Test retrieving high scores for a specific user."""
        self.leaderboard_service.save_score("Alice", 150)
        self.leaderboard_service.save_score("Alice", 180)
        self.leaderboard_service.save_score("Alice", 120)
        user_scores = self.leaderboard_service.get_user_high_scores("Alice")
        self.assertEqual(user_scores, [180, 150, 120])

    def test_clear_scores(self):
        """Test clearing all scores."""
        self.leaderboard_service.save_score("Alice", 150)
        self.leaderboard_service.save_score("Bob", 200)
        self.leaderboard_service.clear_scores()
        top_scores = self.leaderboard_service.get_top_scores()
        self.assertEqual(len(top_scores), 0)

    def tearDown(self):
        """Clean up resources if needed (optional)."""
        pass


if __name__ == "__main__":
    unittest.main()
