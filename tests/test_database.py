import unittest
from src.database import DatabaseRepository

class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(':memory:')

    def tearDown(self):
        self.repo.close()

    def test_add_success(self):
        result = self.repo.add(1, "user1", "Hello")
        self.assertTrue(result)
        self.assertIsNotNone(self.repo.get_by_id(1))

    def test_add_duplicate_id_raises_error(self):
        self.repo.add(1, "user1", "First")
        with self.assertRaises(ValueError):
            self.repo.add(1, "user2", "Duplicate ID")

    def test_add_invalid_length_raises_error(self):
        with self.assertRaises(ValueError):
            self.repo.add(2, "u" * 300, "Message")

    def test_get_by_id_found(self):
        self.repo.add(10, "admin", "Test msg")
        record = self.repo.get_by_id(10)
        self.assertEqual(record['name'], "admin")
        self.assertEqual(record['message'], "Test msg")

    def test_get_by_id_not_found(self):
        record = self.repo.get_by_id(999)
        self.assertIsNone(record)

    def test_get_by_name_found(self):
        self.repo.add(1, "alice", "Msg 1")
        self.repo.add(2, "bob", "Msg 2")
        self.repo.add(3, "alice", "Msg 3")

        records = self.repo.get_by_name("alice")
        self.assertEqual(len(records), 2)

    def test_get_by_name_empty(self):
        records = self.repo.get_by_name("non_existent_user")
        self.assertEqual(len(records), 0)

    def test_update_success(self):
        self.repo.add(5, "user", "Old text")
        result = self.repo.update(5, "New text")
        self.assertTrue(result)
        self.assertEqual(self.repo.get_by_id(5)['message'], "New text")

    def test_update_not_found(self):
        result = self.repo.update(999, "New text")
        self.assertFalse(result)

    def test_delete_success(self):
        self.repo.add(7, "user", "To delete")
        result = self.repo.delete(7)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(7))

    def test_delete_not_found(self):
        result = self.repo.delete(888)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()