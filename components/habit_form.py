import streamlit as st

def render_habit_form(db):
    st.header("Create New Habit")

    with st.form("habit_form"):
        name = st.text_input("Habit Name")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create Habit")

        if submitted and name:
            db.add_habit(name, description)
            st.success(f"Created new habit: {name}")
            st.rerun()