
from database import get_connection


def register_learner(admission_no, full_name, class_name):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO learners
            (admission_no, full_name, class_name)
            VALUES (?, ?, ?)
        """, (admission_no, full_name, class_name))

        connection.commit()
        return True, "Learner registered successfully!"

    except Exception as error:
        return False, f"Registration failed: {error}"

    finally:
        connection.close()


def get_all_learners():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT learner_id, admission_no, full_name, class_name
        FROM learners
        ORDER BY full_name
    """)

    learners = cursor.fetchall()

    connection.close()

    return learners
