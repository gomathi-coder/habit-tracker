import sqlite3
from datetime import datetime
import pandas as pd

class HabitDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('habits.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS habit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    completed_date DATE,
                    completed INTEGER DEFAULT 1,
                    FOREIGN KEY (habit_id) REFERENCES habits (id),
                    UNIQUE(habit_id, completed_date)
                )
            ''')

    def add_habit(self, name, description):
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO habits (name, description) VALUES (?, ?)',
                (name, description)
            )
            return cursor.lastrowid

    def get_habits(self):
        query = 'SELECT * FROM habits ORDER BY created_at DESC'
        return pd.read_sql_query(query, self.conn)

    def log_habit(self, habit_id, date):
        try:
            with self.conn:
                self.conn.execute(
                    'INSERT OR REPLACE INTO habit_logs (habit_id, completed_date) VALUES (?, ?)',
                    (habit_id, date)
                )
            return True
        except sqlite3.Error:
            return False

    def get_habit_logs(self, habit_id=None, start_date=None, end_date=None):
        query = '''
            SELECT h.name, hl.completed_date, hl.completed
            FROM habits h
            LEFT JOIN habit_logs hl ON h.id = hl.habit_id
            WHERE 1=1
        '''
        params = []
        
        if habit_id:
            query += ' AND h.id = ?'
            params.append(habit_id)
        
        if start_date:
            query += ' AND hl.completed_date >= ?'
            params.append(start_date)
            
        if end_date:
            query += ' AND hl.completed_date <= ?'
            params.append(end_date)
            
        return pd.read_sql_query(query, self.conn, params=params)

    def get_streak(self, habit_id):
        logs = self.get_habit_logs(habit_id)
        if logs.empty:
            return 0

        current_streak = 0
        max_streak = 0
        today = datetime.now().date()

        # Filter out rows where completed_date is None and sort
        valid_logs = logs[logs['completed_date'].notna()].sort_values('completed_date', ascending=False)

        if valid_logs.empty:
            return 0

        for _, row in valid_logs.iterrows():
            log_date = datetime.strptime(row['completed_date'], '%Y-%m-%d').date()
            if (today - log_date).days <= current_streak + 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                break

        return current_streak