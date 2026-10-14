import logging
import unittest

from src.database import Database


def setUpModule():
    logging.disable(logging.CRITICAL)


def tearDownModule():
    logging.disable(logging.NOTSET)


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")

    def tearDown(self):
        self.database.close()

    def test_get_returns_none_when_record_does_not_exist(self):
        self.assertIsNone(self.database.get("3", "4", "5"))

    def test_added_record_is_returned_with_type_and_error(self):
        self.database.add("1", "2", "10", "не треугольник", "текст ошибки")

        self.assertEqual(
            self.database.get("1", "2", "10"),
            ("не треугольник", "текст ошибки")
        )

    def test_add_with_same_sides_overwrites_record(self):
        self.database.add("3", "4", "5", "старый результат", "")
        self.database.add("3", "4", "5", "новый результат", "")

        self.assertEqual(self.database.get("3", "4", "5"), ("новый результат", ""))

    def test_record_is_identified_by_all_three_sides(self):
        self.database.add("3", "4", "5", "первая запись", "")
        self.database.add("5", "4", "3", "вторая запись", "")

        self.assertEqual(self.database.get("3", "4", "5"), ("первая запись", ""))
        self.assertEqual(self.database.get("5", "4", "3"), ("вторая запись", ""))

    def test_delete_removes_record_and_reports_result(self):
        self.database.add("3", "4", "5", "разносторонний", "")

        self.assertTrue(self.database.delete("3", "4", "5"))
        self.assertIsNone(self.database.get("3", "4", "5"))
        self.assertFalse(self.database.delete("3", "4", "5"))


if __name__ == "__main__":
    unittest.main()
