import unittest
from src.services import StudentService, CourseService, QuizService, ProgressService
from src.repository import JsonRepository
from src.models import Student, Course, Quiz, Progress

class TestServices(unittest.TestCase):

    def setUp(self):
        self.student_repo = JsonRepository("Student")
        self.course_repo = JsonRepository("Course")
        self.quiz_repo = JsonRepository("Quiz")
        self.progress_repo = JsonRepository("Progress")

        # Clean files
        self.student_repo._save_data([])
        self.course_repo._save_data([])
        self.quiz_repo._save_data([])
        self.progress_repo._save_data([])

        self.student_service = StudentService(self.student_repo)
        self.course_service = CourseService(self.course_repo)
        self.quiz_service = QuizService(self.quiz_repo)
        self.progress_service = ProgressService(
            self.student_repo, self.quiz_repo, self.progress_repo
        )

    def test_create_student_success(self):
        self.student_service.create_student("S001", "Alice", "alice@test.com")
        data = self.student_repo.get_by_id("S001")
        self.assertEqual(data["name"], "Alice")

    def test_create_progress_invalid_student(self):
        self.course_service.create_course("C01", "Python", "Dr. Lee")
        self.quiz_service.create_quiz("Q01", "C01", "Final", 100)
        with self.assertRaises(ValueError):
            self.progress_service.create_progress("P01", "NON", "Q01", 50)

    def test_create_progress_invalid_score(self):
        self.student_service.create_student("S002", "Bob", "bob@test.com")
        self.course_service.create_course("C02", "Math", "Dr. X")
        self.quiz_service.create_quiz("Q02", "C02", "Quiz1", 50)
        with self.assertRaises(ValueError):
            self.progress_service.create_progress("P02", "S002", "Q02", 100)  # > max_score

    def test_update_progress_out_of_range(self):
        self.student_service.create_student("S003", "Charlie", "charlie@test.com")
        self.course_service.create_course("C03", "Science", "Dr. Y")
        self.quiz_service.create_quiz("Q03", "C03", "Quiz2", 30)
        self.progress_service.create_progress("P03", "S003", "Q03", 20)
        with self.assertRaises(ValueError):
            self.progress_service.update_progress("P03", 50)

if __name__ == "__main__":
    unittest.main()
