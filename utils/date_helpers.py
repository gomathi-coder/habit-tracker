from datetime import datetime, timedelta

def get_date_range(days):
    """Return a list of dates for the last n days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    date_range = []
    
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    return date_range

def format_date(date):
    """Format date for display"""
    return date.strftime('%Y-%m-%d')
