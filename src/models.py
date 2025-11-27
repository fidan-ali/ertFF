import uuid
from abc import ABC, abstractmethod

# --- Base Class (Inheritance) ---
class BaseModel(ABC):
    def __init__(self, id_val=None):
        # If an ID is provided, use it; otherwise generate a new one
        self._id = id_val if id_val else str(uuid.uuid4())

    def get_id(self):
        return self._id

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def display_details(self):
        pass

# --- Student Class ---
class Student(BaseModel):
    def __init__(self, student_id, name, email):
        super().__init__(student_id)
        self._name = name
        self._email = email

    def display_details(self):
        return f"Student: {self._name} | Email: {self._email} | ID: {self._id}"

    def to_dict(self):
        # We use generic 'id' key to make the Repository easier to write
        return {'id': self._id, 'name': self._name, 'email': self._email}

# --- Course Class ---
class Course(BaseModel):
    def __init__(self, course_id, title, instructor):
        super().__init__(course_id)
        self._title = title
        self._instructor = instructor

    def display_details(self):
        return f"Course: {self._title} | Instructor: {self._instructor} | ID: {self._id}"

    def to_dict(self):
        return {'id': self._id, 'title': self._title, 'instructor': self._instructor}

# --- Quiz Class ---
class Quiz(BaseModel):
    def __init__(self, quiz_id, course_id, title, max_score):
        super().__init__(quiz_id)
        self._course_id = course_id
        self._title = title
        self._max_score = max_score

    def display_details(self):
        return f"Quiz: {self._title} (Max: {self._max_score}) | Course ID: {self._course_id}"

    def to_dict(self):
        return {'id': self._id, 'course_id': self._course_id, 'title': self._title, 'max_score': self._max_score}

# --- Progress Class ---
class Progress(BaseModel):
    def __init__(self, progress_id, student_id, quiz_id, score):
        super().__init__(progress_id)
        self._student_id = student_id
        self._quiz_id = quiz_id
        self._score = score

    def display_details(self):
        return f"Progress: Score {self._score} | Student ID: {self._student_id}"

    def to_dict(self):
        return {'id': self._id, 'student_id': self._student_id, 'quiz_id': self._quiz_id, 'score': self._score}