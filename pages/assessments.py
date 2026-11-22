
import streamlit as st
import pandas as pd
from datetime import date

from services import (
    record_assessment,
    get_all_assessments,
    get_all_learners,
    get_all_subjects
)

st.title("📝 Assessment Management")

st.write("Record and manage learner assessments.")

# Record assessment
st.subheader("Record New Assessment")

learners = get_all_learners()
subjects = get_all_subjects()

if not learners:
    st.warning("Please register learners first.")
elif not subjects:
    st.warning("Please add subjects first.")
else:
    with st.form("assessment_form"):

        learner_options = {
            f"{learner[1]} - {learner[2]}": learner[0]
            for learner in learners
        }

        subject_options = {
            subject[1]: subject[0]
            for subject in subjects
        }

        learner = st.selectbox(
            "Select Learner",
            options=list(learner_options.keys())
        )

        subject = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys())
        )

        assessment_name = st.text_input(
            "Assessment Name",
            placeholder="e.g. End Term Examination"
        )

        col1, col2 = st.columns(2)

        with col1:
            score = st.number_input(
                "Score",
                min_value=0.0,
                value=0.0
            )

        with col2:
            max_score = st.number_input(
                "Maximum Score",
                min_value=0.1,
                max_value=100.0,
                value=100.0
            )

        assessment_date = st.date_input(
            "Assessment Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Save Assessment",
            use_container_width=True
        )

        if submitted:
            success, message = record_assessment(
                learner_options[learner],
                subject_options[subject],
                assessment_name,
                score,
                max_score,
                assessment_date
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

# Display assessment records
st.divider()
st.subheader("Assessment Records")

records = get_all_assessments()

if records:
    columns = [
        "Admission Number",
        "Learner Name",
        "Class",
        "Subject",
        "Assessment",
        "Score",
        "Maximum Score",
        "Date"
    ]

    df = pd.DataFrame(records, columns=columns)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Assessment Records",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="assessment_records.csv",
        mime="text/csv"
    )
else:
    st.info("No assessment records available.")
