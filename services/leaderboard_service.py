import sqlite3
from typing import List, Tuple

DATABASE_NAME = 'leaderboard.db'


class LeaderboardService:
    def __init__(self, db_name: str = DATABASE_NAME, connection=None):
        self.db_name = db_name
        self.connection = connection or sqlite3.connect(self.db_name)
        self._initialize_database()

    def _initialize_database(self):
        """Initializes the SQLite database and creates the scores table if it doesn't exist."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()
        print("Database initialized.")

    def save_score(self, username: str, score: int):
        """Saves a player's score to the database."""
        print(f"Attempting to save score: {username} - {score}")
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO scores (username, score) VALUES (?, ?)
        ''', (username, score))
        self.connection.commit()
        print("Score saved successfully.")

    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Retrieves the top `limit` scores from all players."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT username, MAX(score) as max_score
            FROM scores
            GROUP BY username
            ORDER BY max_score DESC
            LIMIT ?
        ''', (limit,))
        top_scores = cursor.fetchall()
        print(f"Retrieved top {limit} scores.")
        return top_scores

    def get_user_high_scores(self, username: str) -> List[int]:
        """Retrieves all high scores for a specific user."""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT score FROM scores
            WHERE username = ?
            ORDER BY score DESC
        ''', (username,))
        user_scores = cursor.fetchall()
        print(f"Retrieved high scores for user: {username}")
        return [score[0] for score in user_scores]

    def clear_scores(self):
        """Clears all scores from the database."""
        cursor = self.connection.cursor()
        cursor.execute('''
            DELETE FROM scores
        ''')
        self.connection.commit()
        print("All scores cleared.")

    def close(self):
        """Closes the database connection."""
        self.connection.close()