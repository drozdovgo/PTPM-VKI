import sqlite3


class DatabaseRepository:
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

    def _validate_string(self, value, max_len, field_name):
        if not isinstance(value, str):
            raise TypeError(f"Поле '{field_name}' должно быть строкой (str).")
        if len(value) > max_len:
            raise ValueError(f"Длина поля '{field_name}' не может превышать {max_len} символов.")

    def get_by_id(self, comment_id):
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int).")

        cursor = self.conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username):
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой (str).")

        cursor = self.conn.execute("SELECT * FROM comments WHERE name = ?", (username,))
        return [dict(row) for row in cursor.fetchall()]

    def add(self, comment_id, username, message):
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int).")

        self._validate_string(username, 256, "username")
        self._validate_string(message, 8096, "message")

        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                    (comment_id, username, message)
                )
            return True
        except sqlite3.IntegrityError:
            raise ValueError(f"Запись с id={comment_id} уже существует.")

    def update(self, comment_id, new_message):
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int).")
        self._validate_string(new_message, 8096, "new_message")

        with self.conn:
            cursor = self.conn.execute(
                "UPDATE comments SET message = ? WHERE id = ?",
                (new_message, comment_id)
            )
        return cursor.rowcount > 0

    def delete(self, comment_id):
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int).")

        with self.conn:
            cursor = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        return cursor.rowcount > 0

    def close(self):
        self.conn.close()