
import streamlit as st
import pandas as pd

from services import add_subject, get_all_subjects

st.title("📚 Subject Management")

st.write("Register and manage school subjects.")

# Add subject
st.subheader("Register New Subject")

with st.form("subject_form"):

    subject_name = st.text_input(
        "Subject Name",
        placeholder="e.g. Mathematics"
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


# Display subjects
st.divider()

st.subheader("Registered Subjects")

subjects = get_all_subjects()

if subjects:

    df = pd.DataFrame(
        subjects,
        columns=["Subject ID", "Subject Name"]
    )

    st.metric("Total Subjects", len(df))

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Subjects",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="school_subjects.csv",
        mime="text/csv"
    )

else:
    st.info("No subjects have been registered yet.")
