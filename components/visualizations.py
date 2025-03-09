import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def render_visualizations(db):
    st.header("Habits Overview")
    
    # Get all habits and their logs for the last 30 days
    habits = db.get_habits()
    if habits.empty:
        return
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    logs = db.get_habit_logs(start_date=start_date, end_date=end_date)
    
    # Completion rate by habit
    if not logs.empty:
        completion_rates = logs.groupby('name')['completed'].mean() * 100
        fig_completion = px.bar(
            completion_rates,
            orientation='h',
            title='Habit Completion Rates (Last 30 Days)',
            labels={'value': 'Completion Rate (%)', 'name': 'Habit'}
        )
        st.plotly_chart(fig_completion)
        
        # Calendar heatmap
        fig_calendar = go.Figure()
        
        for habit_name in habits['name']:
            habit_logs = logs[logs['name'] == habit_name]
            dates = pd.date_range(start_date, end_date)
            values = [1 if date.strftime('%Y-%m-%d') in habit_logs['completed_date'].values else 0 
                     for date in dates]
            
            fig_calendar.add_trace(go.Heatmap(
                x=dates,
                y=[habit_name] * len(dates),
                z=[values],
                colorscale=[[0, '#F2F4F4'], [1, '#FF4B4B']],
                showscale=False
            ))
            
        fig_calendar.update_layout(
            title='Habit Completion Calendar',
            xaxis_title='Date',
            yaxis_title='Habit',
            height=100 + (len(habits) * 30)
        )
        
        st.plotly_chart(fig_calendar)
