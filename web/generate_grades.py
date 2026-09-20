import random
import os
import psycopg

# Base directory of the current file (web/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root directory (CTF-TUCaN/)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://tucan:tucan@db:5432/tucan")


# Possible grade values and their weighted distribution
# Weights are chosen to simulate a realistic grading curve
GRADES = ["1.0", "1.3", "1.7", "2.0", "2.3", "2.7", "3.0", "3.3", "3.7", "4.0", "5.0"]
GRADE_WEIGHTS = [2, 3, 6, 8, 8, 12, 12, 10, 10, 9, 10]


def generate_grades():
    """
    Generates random grades for each student across a random
    subset of available courses.
    Intended to be executed once during initial setup or if database reset is needed.
    """
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Fetch all student accounts
    cursor.execute("SELECT id FROM users WHERE role = 'student'")
    students = cursor.fetchall()

    # Fetch all available courses
    cursor.execute("SELECT id FROM courses")
    courses = [row[0] for row in cursor.fetchall()]

    inserted = 0

    for (student_id,) in students:
        # Each student is assigned a random number of courses
        selected_courses = random.sample(courses, random.randint(2, 12))

        for course_id in selected_courses:
            # Grade selection follows a weighted distribution
            grade = random.choices(GRADES, weights=GRADE_WEIGHTS, k=1)[0]

            cursor.execute(
                """
                INSERT INTO grades (student_id, course_id, grade)
                VALUES (%s, %s, %s)
                """,
                (student_id, course_id, grade)
            )
            inserted += 1

    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_grades()
