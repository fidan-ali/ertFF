import unittest
import uuid
from src.models import Student, Course, Quiz, Progress, BaseModel

class TestModels(unittest.TestCase):

    # --- BaseModel ---
    def test_base_model_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            BaseModel()

    def test_student_auto_id(self):
        student = Student(student_id=None, name="Alice", email="alice@test.com")
        self.assertIsNotNone(student.get_id())
        # Check UUID validity
        self.assertIsInstance(uuid.UUID(student.get_id()), uuid.UUID)

    def test_student_provided_id(self):
        student = Student(student_id="S001", name="Bob", email="bob@test.com")
        self.assertEqual(student.get_id(), "S001")

    # --- Student ---
    def test_student_to_dict(self):
        student = Student(student_id="S002", name="Charlie", email="charlie@test.com")
        self.assertEqual(student.to_dict(), {
            "id": "S002",
            "name": "Charlie",
            "email": "charlie@test.com"
        })

    def test_student_empty_name(self):
        with self.assertRaises(ValueError):
            Student(student_id="S003", name="", email="test@test.com")

    def test_student_empty_email(self):
        with self.assertRaises(ValueError):
            Student(student_id="S004", name="Name", email="")

    # --- Course ---
    def test_course_to_dict(self):
        course = Course(course_id="C101", title="Python", instructor="Dr. Lee")
        self.assertEqual(course.to_dict(), {
            "id": "C101",
            "title": "Python",
            "instructor": "Dr. Lee"
        })

    # --- Quiz ---
    def test_quiz_to_dict(self):
        quiz = Quiz(quiz_id="Q01", course_id="C101", title="Test", max_score=100)
        self.assertEqual(quiz.to_dict(), {
            "id": "Q01",
            "course_id": "C101",
            "title": "Test",
            "max_score": 100
        })

    # --- Progress ---
    def test_progress_to_dict(self):
        progress = Progress(progress_id="P01", student_id="S01", quiz_id="Q01", score=80)
        self.assertEqual(progress.to_dict(), {
            "id": "P01",
            "student_id": "S01",
            "quiz_id": "Q01",
            "score": 80
        })

if __name__ == "__main__":
    unittest.main()
