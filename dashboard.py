#!/usr/bin/env python3
"""
Katbus Onboarding Dashboard

Web-based dashboard for managers to track employee onboarding progress
with real-time updates and detailed analytics.
"""

import sqlite3
import json
from typing import Dict, List, Optional
from flask import Flask, render_template, jsonify
import plotly.graph_objs as go
import plotly.utils
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

class OnboardingDashboard:
    def __init__(self, db_path: str = "onboarding.db"):
        self.db_path = db_path
    
    def get_all_progress(self) -> List[Dict]:
        """Get progress for all employees."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT employee_id, employee_name, slack_user_id, start_date,
                   current_step, completion_percentage, completed_date,
                   last_activity, step_1_github, step_2_environment,
                   step_3_history_quiz, step_4_product_quiz,
                   step_5_team_integration, step_6_technical_setup,
                   step_7_app_testing, step_8_first_contribution
            FROM onboarding_progress
            ORDER BY start_date DESC
        ''')
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_analytics_data(self) -> Dict:
        """Get analytics data for dashboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM onboarding_progress')
        total_employees = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM onboarding_progress WHERE completion_percentage = 100')
        completed_employees = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(completion_percentage) FROM onboarding_progress')
        avg_completion = cursor.fetchone()[0] or 0
        
        step_completion = {}
        steps = [
            ('step_1_github', 'GitHub Account'),
            ('step_2_environment', 'Dev Environment'),
            ('step_3_history_quiz', 'History Quiz'),
            ('step_4_product_quiz', 'Product Quiz'),
            ('step_5_team_integration', 'Team Integration'),
            ('step_6_technical_setup', 'Technical Setup'),
            ('step_7_app_testing', 'App Testing'),
            ('step_8_first_contribution', 'First Contribution')
        ]
        
        for step_field, step_name in steps:
            if 'quiz' in step_field:
                min_score = 3 if 'history' in step_field else 2
                cursor.execute(f'SELECT COUNT(*) FROM onboarding_progress WHERE {step_field} >= ?', (min_score,))
            else:
                cursor.execute(f'SELECT COUNT(*) FROM onboarding_progress WHERE {step_field} = 1')
            
            completed = cursor.fetchone()[0]
            step_completion[step_name] = {
                'completed': completed,
                'total': total_employees,
                'percentage': (completed / total_employees * 100) if total_employees > 0 else 0
            }
        
        cursor.execute('''
            SELECT DATE(start_date) as date, COUNT(*) as count
            FROM onboarding_progress
            WHERE start_date >= date('now', '-30 days')
            GROUP BY DATE(start_date)
            ORDER BY date
        ''')
        
        daily_starts = cursor.fetchall()
        
        cursor.execute('''
            SELECT AVG(julianday(completed_date) - julianday(start_date)) as avg_days
            FROM onboarding_progress
            WHERE completed_date IS NOT NULL
        ''')
        
        avg_completion_days = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_employees': total_employees,
            'completed_employees': completed_employees,
            'avg_completion': avg_completion,
            'completion_rate': (completed_employees / total_employees * 100) if total_employees > 0 else 0,
            'step_completion': step_completion,
            'daily_starts': daily_starts,
            'avg_completion_days': avg_completion_days
        }
    
    def get_employee_details(self, employee_id: str) -> Optional[Dict]:
        """Get detailed information for a specific employee."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM onboarding_progress WHERE employee_id = ?
        ''', (employee_id,))
        
        result = cursor.fetchone()
        if result:
            columns = [desc[0] for desc in cursor.description]
            employee_data = dict(zip(columns, result))
            
            cursor.execute('''
                SELECT quiz_type, score, total_questions, attempt_date
                FROM quiz_attempts
                WHERE employee_id = ?
                ORDER BY attempt_date DESC
            ''', (employee_id,))
            
            quiz_attempts = cursor.fetchall()
            employee_data['quiz_attempts'] = [
                {
                    'quiz_type': attempt[0],
                    'score': attempt[1],
                    'total_questions': attempt[2],
                    'attempt_date': attempt[3],
                    'percentage': (attempt[1] / attempt[2] * 100) if attempt[2] > 0 else 0
                }
                for attempt in quiz_attempts
            ]
            
            conn.close()
            return employee_data
        
        conn.close()
        return None

dashboard = OnboardingDashboard()

@app.route('/')
def index():
    """Main dashboard page."""
    progress_data = dashboard.get_all_progress()
    analytics = dashboard.get_analytics_data()
    
    return render_template('dashboard.html', 
                         progress_data=progress_data,
                         analytics=analytics)

@app.route('/api/progress')
def api_progress():
    """API endpoint for progress data."""
    return jsonify(dashboard.get_all_progress())

@app.route('/api/analytics')
def api_analytics():
    """API endpoint for analytics data."""
    return jsonify(dashboard.get_analytics_data())

@app.route('/api/employee/<employee_id>')
def api_employee_details(employee_id):
    """API endpoint for employee details."""
    employee_data = dashboard.get_employee_details(employee_id)
    if employee_data:
        return jsonify(employee_data)
    return jsonify({'error': 'Employee not found'}), 404

@app.route('/employee/<employee_id>')
def employee_details(employee_id):
    """Employee details page."""
    employee_data = dashboard.get_employee_details(employee_id)
    if not employee_data:
        return "Employee not found", 404
    
    return render_template('employee_details.html', employee=employee_data)

@app.route('/api/charts/completion_progress')
def completion_progress_chart():
    """Generate completion progress chart data."""
    analytics = dashboard.get_analytics_data()
    
    steps = list(analytics['step_completion'].keys())
    percentages = [analytics['step_completion'][step]['percentage'] for step in steps]
    
    fig = go.Figure(data=[
        go.Bar(
            x=steps,
            y=percentages,
            marker_color=['#FF6B9D', '#C44569', '#F8B500', '#6C5CE7', '#A29BFE', '#74B9FF', '#00CEC9', '#55A3FF'],
            text=[f"{p:.1f}%" for p in percentages],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Step Completion Rates',
        xaxis_title='Onboarding Steps',
        yaxis_title='Completion Percentage',
        template='plotly_white',
        height=400
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/charts/daily_starts')
def daily_starts_chart():
    """Generate daily starts chart data."""
    analytics = dashboard.get_analytics_data()
    
    dates = [item[0] for item in analytics['daily_starts']]
    counts = [item[1] for item in analytics['daily_starts']]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=dates,
            y=counts,
            mode='lines+markers',
            line=dict(color='#6C5CE7', width=3),
            marker=dict(size=8, color='#A29BFE')
        )
    ])
    
    fig.update_layout(
        title='Daily Onboarding Starts (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='New Employees',
        template='plotly_white',
        height=300
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
