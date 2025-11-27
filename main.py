# main.py
# This file is the Application Entry Point and acts as the Controller.

# Import dependencies from the specific locations in the src/ folder:
from src.factory import EntityFactory
from src.repository import JsonRepository
from src.utils import input_non_empty, input_optional_id, input_number, input_alpha_spaces 
# Note: clear_screen function is currently not imported as it's not strictly necessary for core logic.

# --- The App Logic (Controller) ---
def run():
    # Initialize Repositories for data persistence
    student_repo = JsonRepository("Student")
    course_repo = JsonRepository("Course")
    quiz_repo = JsonRepository("Quiz")
    progress_repo = JsonRepository("Progress")

    while True:
        print("\n=== E-LEARNING MENU ===")
        print("1. Add Student (Create)")
        print("2. Add Course (Create)")
        print("3. Add Quiz (Create)")
        print("4. Add Progress Record (Create)")
        print("-----------------------")
        print("5. View Student Details (Read)")
        print("6. View Course Details (Read)")
        print("7. View Quiz Details (Read)")
        print("8. View Progress Record (Read)")
        print("-----------------------")
        print("9. Exit")
        
        choice = input("Select option: ")
        print("-----------------------")

        # --- CREATE Operations (Options 1-4) ---

        if choice == "1":
            print("--- Add Student ---")
            sid = input_optional_id("Student ID (Enter for auto): ")
            name = input_alpha_spaces("Name (letters/spaces only): ") 
            email = input_non_empty("Email: ")
            try:
                student = EntityFactory.create_entity('Student', id=sid, name=name, email=email)
                student_repo.create(student)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("--- Add Course ---")
            cid = input_optional_id("Course ID (Enter for auto): ")
            title = input_alpha_spaces("Title (letters/spaces only): ")
            instructor = input_alpha_spaces("Instructor (letters/spaces only): ") 
            try:
                course = EntityFactory.create_entity('Course', id=cid, title=title, instructor=instructor)
                course_repo.create(course)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print("--- Add Quiz ---")
            qid = input_optional_id("Quiz ID (Enter for auto): ")
            cid = input_non_empty("Course ID this quiz belongs to: ")
            title = input_non_empty("Quiz Title: ")
            max_score = input_number("Max Score (number): ")
            try:
                # OPTIONAL: Add a check here if the Course ID exists before creating the quiz
                quiz = EntityFactory.create_entity('Quiz', id=qid, course_id=cid, title=title, max_score=max_score)
                quiz_repo.create(quiz)
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            print("--- Add Progress Record ---")
            pid = input_optional_id("Progress ID (Enter for auto): ")
            sid = input_non_empty("Student ID who took the quiz: ")
            qid = input_non_empty("Quiz ID the score is for: ")
            score = input_number("Score received (number): ")
            
            try:
                # 1. CHECK STUDENT EXISTENCE (Referential Integrity Check)
                student_data = student_repo.get_by_id(sid)
                if not student_data:
                    raise ValueError(f"❌ Cannot create Progress: Student ID '{sid}' does not exist.")

                # 2. CHECK QUIZ EXISTENCE (Referential Integrity Check)
                quiz_data = quiz_repo.get_by_id(qid)
                if not quiz_data:
                    raise ValueError(f"❌ Cannot create Progress: Quiz ID '{qid}' does not exist.")
                
                # Get max score for validation
                max_score = quiz_data.get('max_score')
                
                # 3. CHECK SCORE RANGE (Business Logic Check)
                if score < 0 or score > max_score:
                    raise ValueError(f"❌ Score must be between 0 and the Quiz maximum ({max_score}).")

                # If all checks pass:
                prog = EntityFactory.create_entity('Progress', id=pid, student_id=sid, quiz_id=qid, score=score)
                progress_repo.create(prog)
            except ValueError as e:
                print(f"Error: {e}")

        # --- READ Operations (Options 5-8) ---
        
        elif choice == "5":
            sid = input_non_empty("Enter Student ID to view: ")
            data = student_repo.get_by_id(sid)
            if data:
                student = EntityFactory.create_entity('Student', **data)
                print(f"\nRESULT: {student.display_details()}")
            else:
                print("❌ Student not found.")
        
        elif choice == "6":
            cid = input_non_empty("Enter Course ID to view: ")
            data = course_repo.get_by_id(cid)
            if data:
                course = EntityFactory.create_entity('Course', **data)
                print(f"\nRESULT: {course.display_details()}")
            else:
                print("❌ Course not found.")

        elif choice == "7":
            qid = input_non_empty("Enter Quiz ID to view: ")
            data = quiz_repo.get_by_id(qid)
            if data:
                quiz = EntityFactory.create_entity('Quiz', **data)
                print(f"\nRESULT: {quiz.display_details()}")
            else:
                print("❌ Quiz not found.")

        elif choice == "8":
            pid = input_non_empty("Enter Progress ID to view: ")
            data = progress_repo.get_by_id(pid)
            if data:
                prog = EntityFactory.create_entity('Progress', **data)
                print(f"\nRESULT: {prog.display_details()}")
            else:
                print("❌ Progress record not found.")

        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    run()