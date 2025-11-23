import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or []
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        return self

    def execute(self):
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type:
            print(f"Error: {exc_val}")
        return False  # لا تخفي الاستثناءات

# ✅ تجربة مدير السياق
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as executor:
        results = executor.execute()
        print(results)
