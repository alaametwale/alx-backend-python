#!/usr/bin/python3
import sqlite3

class DatabaseConnection:
    """Custom class-based context manager for handling DB connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open the database connection and return it."""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection safely, handling errors."""
        if self.connection:
            if exc_type:
                self.connection.rollback()
                print("Transaction rolled back due to an error.")
            else:
                self.connection.commit()
            self.connection.close()
            print("Database connection closed.")

# Usage example
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
