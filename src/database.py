import logging
import sqlite3


class Database:

    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS triangles ("
            "side_a TEXT, side_b TEXT, side_c TEXT, "
            "triangle_type TEXT, error_message TEXT, "
            "PRIMARY KEY (side_a, side_b, side_c))"
        )
        self.connection.commit()
        logging.debug(f"БД подключена: {db_path}")

    def add(self, a_str, b_str, c_str, kind, error):
        self.connection.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (a_str, b_str, c_str, kind, error)
        )
        self.connection.commit()
        logging.info(f"В БД добавлено: {a_str}, {b_str}, {c_str} -> {kind} {error}")

    def get(self, a_str, b_str, c_str):
        cursor = self.connection.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (a_str, b_str, c_str)
        )
        row = cursor.fetchone()
        if row is None:
            logging.debug(f"В БД нет записи для {a_str}, {b_str}, {c_str}")
            return None
        logging.debug(f"Из БД получено: {row}")
        return row

    def delete(self, a_str, b_str, c_str):
        cursor = self.connection.execute(
            "DELETE FROM triangles "
            "WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (a_str, b_str, c_str)
        )
        self.connection.commit()
        logging.info(f"Из БД удалено записей: {cursor.rowcount}")
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()
