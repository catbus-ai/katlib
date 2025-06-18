#!/usr/bin/env python3
"""
Quick Start Script for Katbus Slack Onboarding System

This script helps you get the Slack onboarding bot running quickly
by checking prerequisites and guiding you through the setup process.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import slack_bolt
        import flask
        import plotly
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements_slack.txt")
        return False

def check_env_variables():
    """Check if Slack environment variables are set"""
    required_vars = [
        'SLACK_BOT_TOKEN',
        'SLACK_SIGNING_SECRET', 
        'SLACK_APP_TOKEN'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nCreate a .env file with:")
        for var in missing_vars:
            print(f"   {var}=your-token-here")
        return False
    
    print("✅ All Slack environment variables are set")
    return True

def initialize_database():
    """Initialize the SQLite database"""
    try:
        from slack_bot import OnboardingDatabase
        db = OnboardingDatabase()
        db.init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_demo_employee():
    """Create a demo employee record for testing"""
    try:
        from slack_bot import OnboardingDatabase
        db = OnboardingDatabase()
        
        existing = db.get_employee_progress("DEMO_USER_123")
        if existing:
            print("✅ Demo employee already exists")
            return True
            
        employee_id = db.create_employee_record("DEMO_USER_123", "Demo Employee")
        print("✅ Demo employee created for testing")
        return True
    except Exception as e:
        print(f"❌ Failed to create demo employee: {e}")
        return False

def run_system_check():
    """Run comprehensive system check"""
    print("🚀 Katbus Slack Onboarding System - Quick Start Check\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_env_variables),
        ("Database", initialize_database),
        ("Demo Data", create_demo_employee)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All checks passed! System is ready to run.")
        print("\n🚀 Next Steps:")
        print("1. Start the Slack bot: python slack_bot.py")
        print("2. Start the dashboard: python dashboard.py")
        print("3. In Slack, use: /onboard @username")
        print("\n📊 Dashboard will be available at: http://localhost:5000")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📖 See setup_instructions.md for detailed setup guide")
    
    return all_passed

def show_slack_setup_guide():
    """Show quick Slack app setup guide"""
    print("\n🔧 Slack App Setup Guide:")
    print("1. Go to: https://api.slack.com/apps")
    print("2. Create New App → From scratch")
    print("3. Name: 'Katbus Onboarding Bot'")
    print("4. Add these permissions:")
    print("   - app_mentions:read")
    print("   - channels:read") 
    print("   - chat:write")
    print("   - commands")
    print("   - users:read")
    print("   - users:read.email")
    print("5. Create slash commands:")
    print("   - /onboard")
    print("   - /progress") 
    print("   - /dashboard")
    print("6. Enable Socket Mode and get tokens")
    print("7. Set environment variables in .env file")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--slack-setup":
        show_slack_setup_guide()
    else:
        success = run_system_check()
        if not success:
            print("\n💡 For Slack app setup help, run: python quick_start.py --slack-setup")
