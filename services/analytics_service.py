
import pandas as pd
from database import get_connection


def load_assessment_data():
    """Retrieve assessment records with learner and subject details."""

    connection = get_connection()

    query = """
    SELECT
        l.learner_id,
        l.admission_no,
        l.full_name,
        l.class_name,
        s.subject_name,
        a.assessment_name,
        a.score,
        a.max_score,
        a.date_taken AS assessment_date
    FROM Assessments a
    JOIN Learners l
        ON a.learner_id = l.learner_id
    JOIN Subjects s
        ON a.subject_id = s.subject_id
"""

    try:
        df = pd.read_sql_query(query, connection)
    finally:
        connection.close()

    if df.empty:
        return df

    df["percentage"] = (
        df["score"] / df["max_score"]
    ) * 100

    return df


def learner_performance(df):
    return (
        df.groupby(
            ["learner_id", "admission_no", "full_name", "class_name"],
            as_index=False
        )
        .agg(
            average_score=("percentage", "mean"),
            assessments_taken=("percentage", "count")
        )
        .sort_values("average_score", ascending=False)
    )


def subject_performance(df):
    return (
        df.groupby("subject_name", as_index=False)
        .agg(
            average_score=("percentage", "mean"),
            assessments_taken=("percentage", "count")
        )
        .sort_values("average_score", ascending=False)
    )


def class_performance(df):
    learner_df = learner_performance(df)

    return (
        learner_df.groupby("class_name", as_index=False)
        .agg(
            average_score=("average_score", "mean"),
            learners_assessed=("learner_id", "nunique")
        )
        .sort_values("average_score", ascending=False)
    )
