#!/usr/bin/env python3
"""
Demo Data Generator for Katbus Slack Onboarding System

Creates sample employee records to demonstrate the dashboard functionality.
"""

import random
from datetime import datetime, timedelta
from slack_bot import OnboardingDatabase, OnboardingStep

def create_demo_employees():
    """Create demo employee records with various progress levels"""
    db = OnboardingDatabase()
    db.init_database()
    
    demo_employees = [
        {
            'slack_user_id': 'U001TEMPEST',
            'name': 'Tempest Storm',
            'progress': 3,  # Currently on step 3
            'scores': {'history': 3, 'product': 0}
        },
        {
            'slack_user_id': 'U002ALEX',
            'name': 'Alex Chen',
            'progress': 8,  # Completed all steps
            'scores': {'history': 4, 'product': 3}
        },
        {
            'slack_user_id': 'U003JORDAN',
            'name': 'Jordan Kim',
            'progress': 5,  # Mid-way through
            'scores': {'history': 4, 'product': 2}
        },
        {
            'slack_user_id': 'U004RILEY',
            'name': 'Riley Martinez',
            'progress': 1,  # Just started
            'scores': {'history': 0, 'product': 0}
        },
        {
            'slack_user_id': 'U005SAGE',
            'name': 'Sage Thompson',
            'progress': 6,  # Almost done
            'scores': {'history': 3, 'product': 3}
        }
    ]
    
    print("🎭 Creating demo employee records...")
    
    for employee in demo_employees:
        existing = db.get_employee_progress(employee['slack_user_id'])
        if existing:
            print(f"   ⏭️  {employee['name']} already exists, skipping...")
            continue
            
        employee_id = db.create_employee_record(
            employee['slack_user_id'], 
            employee['name']
        )
        
        current_step = employee['progress']
        
        for step in range(1, min(current_step + 1, 9)):
            if step == 3:  # History quiz
                db.update_step_completion(
                    employee['slack_user_id'], 
                    step, 
                    True, 
                    employee['scores']['history']
                )
            elif step == 4:  # Product quiz
                db.update_step_completion(
                    employee['slack_user_id'], 
                    step, 
                    True, 
                    employee['scores']['product']
                )
            else:
                db.update_step_completion(
                    employee['slack_user_id'], 
                    step, 
                    True
                )
        
        print(f"   ✅ Created {employee['name']} (Step {current_step}/8)")
    
    print("\n🎉 Demo data created successfully!")
    print("📊 Start the dashboard to see the demo employees: python dashboard.py")
    print("🌐 Then visit: http://localhost:5000")

def clear_demo_data():
    """Clear all demo employee records"""
    db = OnboardingDatabase()
    
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM onboarding_progress WHERE slack_user_id LIKE 'U00%'")
    cursor.execute("DELETE FROM quiz_attempts WHERE employee_id LIKE 'U00%'")
    
    conn.commit()
    conn.close()
    
    print("🧹 Demo data cleared!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_demo_data()
    else:
        create_demo_employees()
