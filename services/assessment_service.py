
from datetime import date
from database import get_connection


def record_assessment(
    learner_id,
    subject_id,
    assessment_name,
    score,
    max_score,
    assessment_date
):
    if not assessment_name or not assessment_name.strip():
        return False, "Assessment name is required."

    assessment_name = assessment_name.strip()

    try:
        score = float(score)
        max_score = float(max_score)

    except (ValueError, TypeError):
        return False, "Scores must be valid numbers."

    if max_score <= 0:
        return False, "Maximum score must be greater than zero."

    if max_score > 100:
        return False, "Maximum score cannot exceed 100."

    if score < 0 or score > max_score:
        return False, "Score must be between zero and maximum score."

    if isinstance(assessment_date, date):
        assessment_date = assessment_date.isoformat()

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Assessments (
                learner_id,
                subject_id,
                assessment_name,
                score,
                max_score,
                date_taken
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            learner_id,
            subject_id,
            assessment_name,
            score,
            max_score,
            assessment_date
        ))

        connection.commit()

        return True, "Assessment recorded successfully."

    except Exception as error:
        connection.rollback()
        return False, f"Could not record assessment: {error}"

    finally:
        connection.close()


def get_all_assessments():

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                l.admission_no,
                l.full_name,
                l.class_name,
                s.subject_name,
                a.assessment_name,
                a.score,
                a.max_score,
                a.date_taken
            FROM Assessments a

            JOIN Learners l
                ON a.learner_id = l.learner_id

            JOIN Subjects s
                ON a.subject_id = s.subject_id

            ORDER BY a.date_taken DESC
        """)

        return cursor.fetchall()

    finally:
        connection.close()
