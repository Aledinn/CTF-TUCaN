from flask import request, session, redirect, render_template, url_for, send_file
from db import get_db
from utils import login_required
import os


def grades_by_id():
    """
    Displays module results for a given student ID.
    If no ID is provided, the request is automatically
    redirected to the currently authenticated student.
    """
    # Enforce student-only access
    if not session.get("user_id") or session.get("role") != "student":
        return redirect("/login")

    student_id = request.args.get("id")

    # Automatically resolve to the authenticated user's ID
    if not student_id:
        return redirect(
            url_for(
                "grades_by_id",
                id=session.get("user_id")
            )
        )

    db = get_db()

    rows = db.execute(
        """
        SELECT
            courses.course_code,
            courses.course_name,
            courses.ects::float8 AS ects,
            courses.semester,
            grades.grade::float8 AS grade
        FROM grades
        JOIN courses
            ON grades.course_id = courses.id
        WHERE grades.student_id = %s
        """,
        (student_id,)
    ).fetchall()

    # If no grades are found, return an internal placeholder file
    if not rows:
        path = os.path.join(
            os.path.dirname(__file__),
            "internal",
            "dev_todo.txt"
        )
        return send_file(
            path,
            mimetype="text/plain"
        )

    return render_template(
        "modulergebnisse.html",
        grades=rows,
        student_id=student_id
    )
