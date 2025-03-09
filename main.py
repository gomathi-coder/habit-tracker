import streamlit as st
from database import HabitDatabase
from components.habit_form import render_habit_form
from components.habit_list import render_habit_list
from components.visualizations import render_visualizations

# Page config
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_db():
    return HabitDatabase()

db = init_db()

# Main layout
st.title("📊 Habit Tracker")

# Sidebar
with st.sidebar:
    render_habit_form(db)
    
    st.markdown("""
    ### Tips for Success
    - Start small with 1-2 habits
    - Be consistent
    - Track daily
    - Celebrate progress
    """)

# Main content
tab1, tab2 = st.tabs(["Track Habits", "Analytics"])

with tab1:
    render_habit_list(db)
    
with tab2:
    render_visualizations(db)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit | "
    "Track your habits and build a better you!"
)
