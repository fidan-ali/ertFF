import unittest
import os
from src.repository import JsonRepository
from src.models import Student, Course

class TestJsonRepository(unittest.TestCase):

    def setUp(self):
        self.repo = JsonRepository("Student")
        self.repo._save_data([])

    def tearDown(self):
        if os.path.exists(self.repo.file_path):
            os.remove(self.repo.file_path)

    def test_create_and_get(self):
        student = Student(student_id="S001", name="Alice", email="alice@test.com")
        self.repo.create(student)
        data = self.repo.get_by_id("S001")
        self.assertEqual(data["name"], "Alice")

    def test_create_duplicate_id(self):
        student1 = Student(student_id="S002", name="Bob", email="bob@test.com")
        student2 = Student(student_id="S002", name="Bobby", email="bobby@test.com")
        self.repo.create(student1)
        with self.assertRaises(ValueError):
            self.repo.create(student2)

    def test_create_duplicate_email(self):
        student1 = Student(student_id="S003", name="Charlie", email="charlie@test.com")
        student2 = Student(student_id="S004", name="Chuck", email="charlie@test.com")
        self.repo.create(student1)
        with self.assertRaises(ValueError):
            self.repo.create(student2)

    def test_update_nonexistent(self):
        with self.assertRaises(ValueError):
            self.repo.update("S999", {"name": "Nobody"})

    def test_delete_nonexistent(self):
        with self.assertRaises(ValueError):
            self.repo.delete("S999")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id("NON_EXIST"))

if __name__ == "__main__":
    unittest.main()
