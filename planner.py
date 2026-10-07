from datetime import date, datetime, timedelta


def calculate_days_remaining(exam_date, today=None):
    if today is None:
        today = date.today()

    if isinstance(exam_date, str):
        exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()

    return max((exam_date - today).days, 0)


def calculate_urgency(days_remaining):
    if days_remaining <= 2:
        return "Very High"
    elif days_remaining <= 5:
        return "High"
    elif days_remaining <= 10:
        return "Medium"
    else:
        return "Low"


def generate_timetable(subjects, available_hours, today=None):
    if today is None:
        today = date.today()

    subject_data = []

    for subject in subjects:
        exam_date = subject["exam_date"]

        if isinstance(exam_date, str):
            exam_date = datetime.strptime(
                exam_date, "%Y-%m-%d"
            ).date()

        subject_data.append({
            "name": subject["name"],
            "exam_date": exam_date
        })

    if not subject_data:
        return []

    # Sort subjects by nearest exam date
    subject_data.sort(
        key=lambda subject: subject["exam_date"]
    )

    latest_exam = max(
        subject["exam_date"]
        for subject in subject_data
    )

    timetable = []
    current_day = today

    while current_day <= latest_exam:

        # Find subjects whose exams have not happened yet
        active_subjects = [
            subject
            for subject in subject_data
            if current_day <= subject["exam_date"]
        ]

        if active_subjects:

            # Subjects with closer exams get higher priority
            active_subjects.sort(
                key=lambda subject: (
                    subject["exam_date"] - current_day
                ).days
            )

            daily_tasks = []

            # Distribute all available hours
            for hour in range(available_hours):

                subject = active_subjects[
                    hour % len(active_subjects)
                ]

                days_left = (
                    subject["exam_date"] - current_day
                ).days

                daily_tasks.append({
                    "subject": subject["name"],
                    "hours": 1,
                    "exam_date": subject["exam_date"].strftime(
                        "%Y-%m-%d"
                    ),
                    "urgency": calculate_urgency(days_left)
                })

            # Combine hours for the same subject
            combined_tasks = {}

            for task in daily_tasks:

                subject_name = task["subject"]

                if subject_name not in combined_tasks:
                    combined_tasks[subject_name] = {
                        "subject": subject_name,
                        "hours": 0,
                        "exam_date": task["exam_date"],
                        "urgency": task["urgency"]
                    }

                combined_tasks[subject_name]["hours"] += 1

            daily_tasks = list(combined_tasks.values())

        else:
            daily_tasks = []

        timetable.append({
            "date": current_day.strftime("%Y-%m-%d"),
            "tasks": daily_tasks
        })

        current_day += timedelta(days=1)

    return timetable


def print_timetable(title, timetable):
    print(f"\n\n{title}")
    print("=" * len(title))

    for day in timetable:
        print(f"\nDate: {day['date']}")

        for task in day["tasks"]:
            print(
                f"  {task['subject']} - "
                f"{task['hours']} hour(s) - "
                f"Exam: {task['exam_date']} - "
                f"Urgency: {task['urgency']}"
            )


if __name__ == "__main__":

    # SAMPLE 1
    subjects1 = [
        {
            "name": "Python",
            "exam_date": "2026-10-15"
        },
        {
            "name": "DBMS",
            "exam_date": "2026-10-18"
        },
        {
            "name": "Mathematics",
            "exam_date": "2026-10-20"
        }
    ]

    timetable1 = generate_timetable(
        subjects1,
        3,
        today=date(2026, 10, 8)
    )

    print_timetable(
        "SAMPLE 1 - SMART STUDY PLANNER",
        timetable1
    )


    # SAMPLE 2
    subjects2 = [
        {
            "name": "C++",
            "exam_date": "2026-10-12"
        },
        {
            "name": "Java",
            "exam_date": "2026-10-16"
        }
    ]

    timetable2 = generate_timetable(
        subjects2,
        2,
        today=date(2026, 10, 8)
    )

    print_timetable(
        "SAMPLE 2 - SMART STUDY PLANNER",
        timetable2
    )


    # SAMPLE 3
    subjects3 = [
        {
            "name": "Data Structures",
            "exam_date": "2026-10-14"
        },
        {
            "name": "Operating Systems",
            "exam_date": "2026-10-19"
        },
        {
            "name": "DBMS",
            "exam_date": "2026-10-22"
        }
    ]

    timetable3 = generate_timetable(
        subjects3,
        4,
        today=date(2026, 10, 8)
    )

    print_timetable(
        "SAMPLE 3 - SMART STUDY PLANNER",
        timetable3
    )