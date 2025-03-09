import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def render_habit_list(db):
    st.header("Track Your Habits")

    # Initialize week offset in session state
    if 'week_offset' not in st.session_state:
        st.session_state.week_offset = 0
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now().date()

    habits = db.get_habits()
    if habits.empty:
        st.info("No habits created yet. Create your first habit above!")
        return

    today = datetime.now().date()

    # Add date picker and week navigation
    col1, col2, col3, col4 = st.columns([1, 2, 3, 1])

    with col1:
        if st.button("← Previous Week"):
            st.session_state.week_offset += 1
            st.rerun()

    with col2:
        # Date picker for quick navigation
        selected_date = st.date_input(
            "Select Week",
            value=today - timedelta(days=7 * st.session_state.week_offset),
            key="week_selector"
        )
        if selected_date != st.session_state.selected_date:
            # Calculate new week offset based on selected date
            days_diff = (today - selected_date).days
            st.session_state.week_offset = days_diff // 7
            st.session_state.selected_date = selected_date
            st.rerun()

    with col3:
        start_date = today - timedelta(days=7 * st.session_state.week_offset + today.weekday())
        end_date = start_date + timedelta(days=6)
        st.write(f"Week: {start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}")

    with col4:
        if st.button("Next Week →"):
            st.session_state.week_offset = max(0, st.session_state.week_offset - 1)
            st.rerun()

    for _, habit in habits.iterrows():
        with st.expander(f"🎯 {habit['name']}", expanded=True):
            st.write(habit['description'])

            # Streak information
            streak = db.get_streak(habit['id'])
            st.metric("Current Streak", f"{streak} days")

            # Calculate number of days to show based on streak
            days_to_show = 7  # Show one week at a time

            # Create columns for the week
            cols = st.columns(days_to_show)

            for i, col in enumerate(cols):
                # Calculate date based on week offset
                date = start_date + timedelta(days=i)
                logs = db.get_habit_logs(habit['id'], date, date)
                completed = not logs.empty and logs['completed'].iloc[0] == 1

                with col:
                    # Show both date and day of week
                    st.write(f"{date.strftime('%d %b')}")
                    st.write(f"{date.strftime('%a')}")
                    if st.button(
                        "✓" if completed else "○",
                        key=f"habit_{habit['id']}_{date}",
                        help=date.strftime('%Y-%m-%d')
                    ):
                        db.log_habit(habit['id'], date)
                        st.rerun()