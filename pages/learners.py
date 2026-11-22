
import streamlit as st
import pandas as pd

from services import (
    register_learner,
    get_all_learners
)

st.title("👨‍🎓 Learner Management")

st.write("Register learners and manage learner records.")

# Registration form
st.subheader("Register New Learner")

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
            "Grade 1",
            "Grade 2",
            "Grade 3",
            "Grade 4",
            "Grade 5",
            "Grade 6",
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


# Display registered learners
st.divider()

st.subheader("Registered Learners")

learners = get_all_learners()

if learners:

    df = pd.DataFrame(
        learners,
        columns=[
            "Learner ID",
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
