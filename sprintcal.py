import streamlit as st

from streamlit_calendar import calendar

st.set_page_config(page_title="Sprint Calendar", page_icon="📆")

from datetime import datetime, timedelta

def generate_sprints(start_date="2024-02-29", sprint_length=14):
    """
    Generate a list of dictionaries representing even and odd numbered sprints.

    Args:
    start_date (str): Start date in the format "YYYY-MM-DD".
    sprint_length (int): Length of each sprint in days.

    Returns:
    list: List of dictionaries representing sprints.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    sprints = []
    sprint_num_offset = 4
    meeting_duration = 1

    for i in range(1, 50):
        sprint_start = start_date + timedelta(days=(i - 1) * sprint_length)
        sprint_end = sprint_start + timedelta(days=sprint_length)
        sprint_num = i + sprint_num_offset

        sprint_type = "Even" if i % 2 == 0 else "Odd"
        color = "#FF6C6C" if i % 2 == 0 else "#FFBD45"

        sprint = {
            #"title": f"Sprint {i} ({sprint_type})",
            "title": f"Sprint {sprint_num} (code)",
            "color": color,
            "start": sprint_start.strftime("%Y-%m-%d"),
            "end": sprint_end.strftime("%Y-%m-%d")
        }

        sprints.append(sprint)

        qa_start = sprint_end
        qa_end = qa_start + timedelta(days=7)  # QA event lasts for one week

        qa_event = {
            "title": f"Sprint {sprint_num} (QA)",
            "color": "#3D9DF3",  # Assuming a different color for QA events
            "start": qa_start.strftime("%Y-%m-%d"),
            "end": qa_end.strftime("%Y-%m-%d")
        }

        sprints.append(qa_event)

        if i % 2 == 0 or (i + 1) % 2 == 0:  # Go/No-Go meetings every three weeks
            go_no_go_time = qa_end + timedelta(days=-1)
            go_no_go_time = go_no_go_time.replace(hour=10, minute=0, second=0)
            meeting_end = go_no_go_time + timedelta(hours=meeting_duration)

            meeting = {
                #"title": f"Spring {i} ({sprint_type})",
                "title": f"S. {sprint_num} (go/no-go)",
                "color": "#3DD56D",
                "start": go_no_go_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end": meeting_end.strftime("%Y-%m-%d %H:%M:%S"),
            }

            sprints.append(meeting)

    return sprints


events = generate_sprints()

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "selectable": "true",
}


# mode = st.selectbox(
#     "Calendar Mode:",
#     (
#         "daygrid",
#         "timegrid",
#         "timeline",
#         "resource-daygrid",
#         "resource-timegrid",
#         "resource-timeline",
#         "list",
#         "multimonth",
#     ),
# )


mode = "daygrid"

if mode == "daygrid":
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth"
        },
        "initialDate": "2024-05-01",
        "initialView": "dayGridMonth",
    }
elif mode == "timegrid":
    calendar_options = {
        **calendar_options,
        "initialView": "timeGridWeek",
    }
elif mode == "timeline":
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "timelineDay,timelineWeek,timelineMonth",
        },
        "initialDate": "2023-07-01",
        "initialView": "timelineMonth",
    }
elif mode == "list":
    calendar_options = {
        **calendar_options,
        "initialDate": "2024-05-01",
        "initialView": "listMonth",
    }
elif mode == "multimonth":
    calendar_options = {
        **calendar_options,
        "initialView": "multiMonthYear",
    }

state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

#st.write(state)