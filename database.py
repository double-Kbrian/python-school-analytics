
import sqlite3
from pathlib import Path

# Always locate database relative to this file
BASE_DIR = Path(__file__).resolve().parent
DATABASE_NAME = BASE_DIR / "school.db"


def get_connection():
    """Establish a connection to the SQLite database."""

    try:
        connection = sqlite3.connect(
            str(DATABASE_NAME),
            timeout=30
        )

        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    except sqlite3.Error as e:

        print(f"Error connecting to database: {e}")

        return None


def create_tables():
    """Create all necessary database tables."""

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    try:

        cursor = connection.cursor()

        # Learners table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Learners (
                learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
                admission_no TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                class_name TEXT NOT NULL
            )
        """)

        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT NOT NULL UNIQUE
            )
        """)

        # Assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Assessments (
                assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                learner_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                assessment_name TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL DEFAULT 100,
                date_taken TEXT NOT NULL,

                FOREIGN KEY (learner_id)
                    REFERENCES Learners(learner_id)
                    ON DELETE CASCADE,

                FOREIGN KEY (subject_id)
                    REFERENCES Subjects(subject_id),

                CHECK (score >= 0),
                CHECK (max_score > 0),
                CHECK (score <= max_score)
            )
        """)

        connection.commit()

        print("Database tables created successfully.")

    except sqlite3.Error as e:

        connection.rollback()

        print(f"Database error: {e}")

        raise

    finally:

        connection.close()


def migrate_database():
    """Upgrade existing database without deleting records."""

    connection = get_connection()

    if connection is None:
        raise RuntimeError("Database connection failed.")

    try:

        cursor = connection.cursor()

        columns = [
            row[1]
            for row in cursor.execute(
                "PRAGMA table_info(Assessments)"
            ).fetchall()
        ]

        if not columns:
            raise RuntimeError(
                "Assessments table does not exist. "
                "Run create_tables() first."
            )

        if "assessment_name" not in columns:

            cursor.execute("""
                ALTER TABLE Assessments
                ADD COLUMN assessment_name TEXT
                NOT NULL DEFAULT 'General Assessment'
            """)

        if "max_score" not in columns:

            cursor.execute("""
                ALTER TABLE Assessments
                ADD COLUMN max_score REAL
                NOT NULL DEFAULT 100
            """)

        connection.commit()

        print("Database migration completed successfully.")

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


if __name__ == "__main__":

    create_tables()
    migrate_database()
