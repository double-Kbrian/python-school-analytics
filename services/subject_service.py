
from database import get_connection


def add_subject(subject_name):
    """Register a new subject."""

    if not subject_name or not subject_name.strip():
        return False, "Subject name is required."

    subject_name = subject_name.strip()

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Subjects (subject_name)
            VALUES (?)
        """, (subject_name,))

        connection.commit()

        return True, "Subject added successfully."

    except Exception as error:
        connection.rollback()
        return False, f"Could not add subject: {error}"

    finally:
        connection.close()


def get_all_subjects():
    """Retrieve all registered subjects."""

    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT subject_id, subject_name
            FROM Subjects
            ORDER BY subject_name
        """)

        return cursor.fetchall()

    finally:
        connection.close()
