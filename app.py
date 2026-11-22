
import streamlit as st
import pandas as pd

from database import create_tables, migrate_database

from services import (
    register_learner,
    get_all_learners,
    add_subject,
    get_all_subjects,
    record_assessment,
    get_all_assessments,
    load_assessment_data,
    learner_performance,
    subject_performance,
    class_performance
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="School Analytics",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

try:
    create_tables()
    migrate_database()

except Exception as error:
    st.error(f"Database initialization failed: {error}")
    st.stop()


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("🎓 School Assessment & Performance Analytics")

st.sidebar.title("School Analytics")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Register Learner",
        "View Learners",
        "Manage Subjects",
        "Record Assessment",
        "View Assessments",
        "Analytics"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.header("School Dashboard")

    learners = get_all_learners()
    subjects = get_all_subjects()
    assessments = get_all_assessments()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Registered Learners",
        len(learners)
    )

    col2.metric(
        "Available Subjects",
        len(subjects)
    )

    col3.metric(
        "Recorded Assessments",
        len(assessments)
    )

    st.divider()

    st.subheader("School Overview")

    if assessments:

        try:
            df = load_assessment_data()

            if not df.empty:

                average = df["percentage"].mean()

                st.metric(
                    "Overall School Average",
                    f"{average:.2f}%"
                )

                subject_data = subject_performance(df)

                st.subheader("Subject Performance Overview")

                st.bar_chart(
                    subject_data.set_index(
                        "subject_name"
                    )["average_score"]
                )

        except Exception as error:
            st.error(f"Could not load school overview: {error}")

    else:
        st.info(
            "Record learner assessments to see school performance statistics."
        )


# ==========================================
# REGISTER LEARNER
# ==========================================

elif menu == "Register Learner":

    st.header("Register a New Learner")

    with st.form("learner_registration"):

        admission_no = st.text_input(
            "Admission Number"
        )

        full_name = st.text_input(
            "Full Name"
        )

        class_name = st.selectbox(
            "Select Class",
            [
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
                "Grade 11",
                "Grade 12"
            ]
        )

        submitted = st.form_submit_button(
            "Register Learner",
            use_container_width=True
        )

        if submitted:

            if not admission_no.strip() or not full_name.strip():

                st.error("Please fill in all required fields.")

            else:

                success, message = register_learner(
                    admission_no,
                    full_name,
                    class_name
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)


# ==========================================
# VIEW LEARNERS
# ==========================================

elif menu == "View Learners":

    st.header("Registered Learners")

    learners = get_all_learners()

    if learners:

        df = pd.DataFrame(
            learners,
            columns=[
                "ID",
                "Admission Number",
                "Full Name",
                "Class"
            ]
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Learners",
            len(df)
        )

        col2.metric(
            "Classes",
            df["Class"].nunique()
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Learner Records",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="learner_records.csv",
            mime="text/csv"
        )

    else:

        st.info("No learners registered yet.")


# ==========================================
# MANAGE SUBJECTS
# ==========================================

elif menu == "Manage Subjects":

    st.header("Subject Management")

    with st.form("subject_form"):

        subject_name = st.text_input(
            "Subject Name"
        )

        submitted = st.form_submit_button(
            "Add Subject",
            use_container_width=True
        )

        if submitted:

            success, message = add_subject(subject_name)

            if success:
                st.success(message)
                st.rerun()

            else:
                st.error(message)

    st.divider()

    st.subheader("Available Subjects")

    subjects = get_all_subjects()

    if subjects:

        df = pd.DataFrame(
            subjects,
            columns=["Subject ID", "Subject Name"]
        )

        st.metric(
            "Total Subjects",
            len(df)
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No subjects added yet.")


# ==========================================
# RECORD ASSESSMENT
# ==========================================

elif menu == "Record Assessment":

    st.header("Record Learner Assessment")

    learners = get_all_learners()
    subjects = get_all_subjects()

    if not learners:

        st.warning(
            "Register learners before recording assessments."
        )

    elif not subjects:

        st.warning(
            "Add subjects before recording assessments."
        )

    else:

        with st.form("assessment_form"):

            selected_learner = st.selectbox(
                "Select Learner",
                learners,
                format_func=lambda x: f"{x[1]} - {x[2]}"
            )

            selected_subject = st.selectbox(
                "Select Subject",
                subjects,
                format_func=lambda x: x[1]
            )

            assessment_name = st.text_input(
                "Assessment Name",
                placeholder="e.g. Mathematics CAT 1"
            )

            col1, col2 = st.columns(2)

            with col1:

                score = st.number_input(
                    "Score Obtained",
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
                "Assessment Date"
            )

            submitted = st.form_submit_button(
                "Save Assessment",
                use_container_width=True
            )

            if submitted:

                success, message = record_assessment(
                    selected_learner[0],
                    selected_subject[0],
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


# ==========================================
# VIEW ASSESSMENTS
# ==========================================

elif menu == "View Assessments":

    st.header("Assessment Records")

    assessments = get_all_assessments()

    if assessments:

        df = pd.DataFrame(
            assessments,
            columns=[
                "Admission Number",
                "Learner",
                "Class",
                "Subject",
                "Assessment",
                "Score",
                "Maximum Score",
                "Date"
            ]
        )

        df["Percentage"] = (
            df["Score"] / df["Maximum Score"] * 100
        ).round(2)

        st.metric(
            "Total Assessment Records",
            len(df)
        )

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

        st.info(
            "No assessments have been recorded yet."
        )


# ==========================================
# ANALYTICS DASHBOARD
# ==========================================

elif menu == "Analytics":

    st.header("📊 School Performance Analytics")

    try:

        df = load_assessment_data()

        if df.empty:

            st.warning(
                "No assessment data available. "
                "Record assessments before viewing analytics."
            )

            st.stop()

        # ----------------------------------
        # PERFORMANCE FILTERS
        # ----------------------------------

        st.subheader("Performance Filters")

        class_options = sorted(
            df["class_name"].dropna().unique().tolist()
        )

        selected_class = st.selectbox(
            "Select Class",
            ["All Classes"] + class_options
        )

        filtered_df = df.copy()

        if selected_class != "All Classes":

            filtered_df = filtered_df[
                filtered_df["class_name"] == selected_class
            ]

        if filtered_df.empty:

            st.info(
                "No assessment records for this selection."
            )

            st.stop()

        # ----------------------------------
        # SUMMARY METRICS
        # ----------------------------------

        learners = learner_performance(filtered_df)

        average = filtered_df["percentage"].mean()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Learners Assessed",
            len(learners)
        )

        col2.metric(
            "Overall Average",
            f"{average:.2f}%"
        )

        col3.metric(
            "Assessment Records",
            len(filtered_df)
        )

        st.divider()

        # ----------------------------------
        # LEARNER PERFORMANCE
        # ----------------------------------

        st.subheader("1. Learner Performance")

        st.dataframe(
            learners[
                [
                    "admission_no",
                    "full_name",
                    "class_name",
                    "average_score",
                    "assessments_taken"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            learners.set_index(
                "full_name"
            )["average_score"]
        )

        # ----------------------------------
        # SUBJECT PERFORMANCE
        # ----------------------------------

        st.subheader("2. Subject Performance")

        subjects = subject_performance(filtered_df)

        st.bar_chart(
            subjects.set_index(
                "subject_name"
            )["average_score"]
        )

        st.dataframe(
            subjects.round(2),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------
        # CLASS PERFORMANCE
        # ----------------------------------

        st.subheader("3. Class Performance")

        classes_df = class_performance(filtered_df)

        st.bar_chart(
            classes_df.set_index(
                "class_name"
            )["average_score"]
        )

        st.dataframe(
            classes_df.round(2),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------
        # ACADEMIC SUPPORT INDICATORS
        # ----------------------------------

        st.subheader(
            "4. Learners Requiring Academic Support"
        )

        support_threshold = st.slider(
            "Academic support indicator (%)",
            min_value=0,
            max_value=100,
            value=50
        )

        support = learners[
            learners["average_score"] < support_threshold
        ]

        if not support.empty:

            st.warning(
                f"{len(support)} learner(s) "
                "are below the selected threshold."
            )

            st.dataframe(
                support[
                    [
                        "admission_no",
                        "full_name",
                        "class_name",
                        "average_score"
                    ]
                ].round(2),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No learners are below the selected threshold."
            )

    except Exception as error:

        st.error(
            f"Unable to load school analytics: {error}"
        )


# ==========================================
# FOOTER
# ==========================================

st.sidebar.markdown("---")
st.sidebar.caption("School Assessment & Analytics System")
