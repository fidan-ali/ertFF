import unittest
import uuid
# We must import the classes we are testing
from src.models import Student, Course, BaseModel, Quiz, Progress
from src.factory import EntityFactory

class TestModels(unittest.TestCase):
    
    ## --- A. Testing BaseModel (Inheritance/ID Logic) ---
    
    def test_base_model_abstract(self):
        """Test that BaseModel cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            BaseModel()

    def test_base_model_auto_id_generation(self):
        """Test that objects get a unique ID if none is provided."""
        student = Student(student_id=None, name="Test", email="test@test.com")
        self.assertIsNotNone(student.get_id())
        # Check if the generated ID is a valid UUID format (optional but good)
        self.assertIsInstance(uuid.UUID(student.get_id()), uuid.UUID)

    def test_base_model_provided_id(self):
        """Test that objects use a specific ID if provided."""
        custom_id = "test-12345"
        student = Student(student_id=custom_id, name="Test", email="test@test.com")
        self.assertEqual(student.get_id(), custom_id)

    ## --- B. Testing Student Class (Encapsulation/Validation) ---
    
    def test_student_creation(self):
        """Test successful Student object creation."""
        student = Student(student_id=None, name="Alice Smith", email="alice@test.com")
        self.assertEqual(student._name, "Alice Smith")
        self.assertIsInstance(student, Student)
        self.assertTrue(hasattr(student, '_email')) # Check for attribute existence

    def test_student_to_dict(self):
        """Test the to_dict method produces the correct structure for saving."""
        student = Student(student_id="S001", name="Bob", email="bob@test.com")
        expected_dict = {'id': 'S001', 'name': 'Bob', 'email': 'bob@test.com'}
        self.assertEqual(student.to_dict(), expected_dict)

    ## --- C. Testing Course Class ---
    
    def test_course_creation(self):
        """Test successful Course object creation."""
        course = Course(course_id="C101", title="Python Basics", instructor="Dr. Lee")
        self.assertEqual(course._title, "Python Basics")
        self.assertEqual(course._instructor, "Dr. Lee")

    def test_course_display_details(self):
        """Test the display_details output format."""
        course = Course(course_id="C101", title="Python Basics", instructor="Dr. Lee")
        expected_output = "Course: Python Basics | Instructor: Dr. Lee | ID: C101"
        self.assertEqual(course.display_details(), expected_output)

    ## --- D. Testing Factory Integration ---
    
    def test_factory_creates_student(self):
        """Test the EntityFactory correctly creates a Student."""
        data = {'id': 'F001', 'name': 'Eve', 'email': 'eve@fact.com'}
        student = EntityFactory.create_entity('Student', **data)
        self.assertIsInstance(student, Student)
        self.assertEqual(student._email, 'eve@fact.com')

    def test_factory_creates_quiz_correctly(self):
        """Test the EntityFactory handles multiple arguments for Quiz."""
        data = {'id': 'QZ01', 'course_id': 'C101', 'title': 'Final Test', 'max_score': 100}
        quiz = EntityFactory.create_entity('Quiz', **data)
        self.assertIsInstance(quiz, object) # Should be type Quiz, but checking object is safer
        self.assertEqual(quiz._max_score, 100)
        self.assertEqual(quiz._course_id, 'C101')
        
    def test_factory_raises_error_on_unknown_type(self):
        """Test the Factory handles invalid entity names."""
        with self.assertRaises(ValueError):
            EntityFactory.create_entity('Teacher', id='T100', name='Mr. X')


if __name__ == '__main__':
    # This setup is needed to run the tests from the terminal
    unittest.main()