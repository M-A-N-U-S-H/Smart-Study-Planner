import streamlit as st
from planner import generate_timetable

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Study Planner")
st.write("Plan your study time and prepare smarter for your exams.")

# -------------------------
# Student Details
# -------------------------
st.header("👨‍🎓 Student Details")

name = st.text_input("Student Name")

# -------------------------
# Study Information
# -------------------------
st.header("⏰ Study Information")

hours = st.number_input(
    "Available Study Hours Per Day",
    min_value=1,
    max_value=24,
    value=5
)

# -------------------------
# Subjects
# -------------------------
st.header("📚 Subjects & Exam Dates")

num_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

for i in range(num_subjects):

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input(
            f"Subject {i + 1}",
            key=f"subject_{i}"
        )

    with col2:
        exam_date = st.date_input(
            f"Exam Date {i + 1}",
            key=f"date_{i}"
        )

    subjects.append({
        "name": subject,
        "exam_date": exam_date
    })

# -------------------------
# Generate Timetable
# -------------------------
if st.button("🚀 Generate Timetable"):

    if not name:
        st.warning("Please enter your name.")

    elif any(not subject["name"] for subject in subjects):
        st.warning("Please enter all subject names.")

    else:

        timetable = generate_timetable(
            subjects,
            hours
        )

        st.success("✅ Timetable generated successfully!")

        st.header("📅 Your Study Timetable")

        for day in timetable:

            st.subheader(f"📆 {day['date']}")

            if day["tasks"]:

                for task in day["tasks"]:

                    st.write(
                        f"📖 **{task['subject']}** — "
                        f"{task['hours']} hour(s) | "
                        f"Exam: {task['exam_date']} | "
                        f"Urgency: **{task['urgency']}**"
                    )

            else:
                st.info("No study tasks for this day.")
# -------------------------
# Progress Checklist
# -------------------------
st.header("📋 Progress Checklist")

st.write("Mark the subjects you have completed:")

for subject in subjects:
    if subject["name"]:
        st.checkbox(
            f"Complete {subject['name']}",
            key=f"progress_{subject['name']}"
        )