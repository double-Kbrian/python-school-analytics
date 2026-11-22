
import streamlit as st
import pandas as pd

import plotly.express as px

from services import (
    load_assessment_data,
    learner_performance,
    subject_performance,
    class_performance
)

# Page configuration
st.set_page_config(
    page_title="School Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 School Analytics Dashboard")
st.markdown("Monitor learner, subject and class performance.")

# Load assessment data
try:
    df = load_assessment_data()

    if df.empty:
        st.warning("No assessment records found.")
        st.stop()

    # Calculate performance
    learners = learner_performance(df)
    subjects = subject_performance(df)
    classes = class_performance(df)

    # KPI metrics
    st.subheader("Overall Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Learners",
        df["learner_id"].nunique()
    )

    col2.metric(
        "Total Subjects",
        df["subject_name"].nunique()
    )

    col3.metric(
        "Assessments",
        len(df)
    )

    col4.metric(
        "Average Score",
        f"{learners['average_score'].mean():.2f}%"
    )

    st.divider()

    # Learner performance
    st.subheader("🏆 Learner Performance")

    st.dataframe(
        learners,
        use_container_width=True,
        hide_index=True
    )

    # Subject performance
    st.subheader("📚 Subject Performance")

    fig_subject = px.bar(
        subjects,
        x="subject_name",
        y="average_score",
        color="average_score",
        title="Average Performance by Subject",
        labels={
            "subject_name": "Subject",
            "average_score": "Average Score (%)"
        }
    )

    st.plotly_chart(
        fig_subject,
        use_container_width=True
    )

    # Class performance
    st.subheader("🏫 Class Performance")

    fig_class = px.bar(
        classes,
        x="class_name",
        y="average_score",
        color="average_score",
        title="Average Performance by Class",
        labels={
            "class_name": "Class",
            "average_score": "Average Score (%)"
        }
    )

    st.plotly_chart(
        fig_class,
        use_container_width=True
    )

    # Assessment records
    st.subheader("📋 Assessment Records")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"Unable to load analytics: {e}")


# INDIVIDUAL LEARNER REPORT

st.divider()
st.header("👤 Individual Learner Report")

# Select learner
learner_options = learners[
    ["learner_id", "admission_no", "full_name", "class_name"]
].drop_duplicates()

selected_learner = st.selectbox(
    "Select Learner",
    learner_options.to_dict("records"),
    format_func=lambda x: (
        f"{x['admission_no']} - {x['full_name']}"
    )
)

# Filter learner records
learner_id = selected_learner["learner_id"]

learner_data = df[
    df["learner_id"] == learner_id
].copy()

# Learner KPIs
learner_average = learner_data["percentage"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Learner",
    selected_learner["full_name"]
)

col2.metric(
    "Overall Average",
    f"{learner_average:.2f}%"
)

col3.metric(
    "Assessments Completed",
    len(learner_data)
)

st.write(
    f"**Admission Number:** "
    f"{selected_learner['admission_no']}"
)

st.write(
    f"**Class:** {selected_learner['class_name']}"
)

# Subject breakdown
st.subheader("Subject Performance")

individual_subjects = (
    learner_data.groupby("subject_name", as_index=False)
    .agg(
        average_score=("percentage", "mean"),
        assessments=("percentage", "count")
    )
)

fig = px.bar(
    individual_subjects,
    x="subject_name",
    y="average_score",
    title="Learner Performance by Subject",
    labels={
        "subject_name": "Subject",
        "average_score": "Average Score (%)"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    individual_subjects.round(2),
    use_container_width=True,
    hide_index=True
)

# Assessment history
st.subheader("Assessment History")

st.dataframe(
    learner_data[
        [
            "subject_name",
            "assessment_name",
            "score",
            "max_score",
            "percentage",
            "assessment_date"
        ]
    ].sort_values("assessment_date"),
    use_container_width=True,
    hide_index=True
)

# Areas requiring attention
st.subheader("Academic Support Indicators")

support_threshold = 50

areas_for_support = individual_subjects[
    individual_subjects["average_score"] < support_threshold
]

if not areas_for_support.empty:

    st.warning(
        "The following subjects may need additional teacher review:"
    )

    st.dataframe(
        areas_for_support,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No subject averages are below the current review threshold."
    )
