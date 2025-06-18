#!/usr/bin/env python3
"""
Katbus Slack Onboarding Bot

Interactive Slack bot that guides new employees through the 8-step onboarding checklist
with progress tracking and automated validation.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass

from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OnboardingStep:
    step_number: int
    title: str
    description: str
    instructions: List[str]
    validation_type: str  # 'manual', 'quiz', 'github', 'screenshot'
    required_score: Optional[int] = None

@dataclass
class QuizQuestion:
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class OnboardingDatabase:
    def __init__(self, db_path: str = "onboarding.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the onboarding database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onboarding_progress (
                employee_id TEXT PRIMARY KEY,
                slack_user_id TEXT UNIQUE,
                employee_name TEXT,
                start_date TIMESTAMP,
                current_step INTEGER DEFAULT 1,
                step_1_github BOOLEAN DEFAULT FALSE,
                step_2_environment BOOLEAN DEFAULT FALSE,
                step_3_history_quiz INTEGER DEFAULT 0,
                step_4_product_quiz INTEGER DEFAULT 0,
                step_5_team_integration BOOLEAN DEFAULT FALSE,
                step_6_technical_setup BOOLEAN DEFAULT FALSE,
                step_7_app_testing BOOLEAN DEFAULT FALSE,
                step_8_first_contribution BOOLEAN DEFAULT FALSE,
                completion_percentage DECIMAL(5,2) DEFAULT 0.00,
                completed_date TIMESTAMP NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT,
                quiz_type TEXT,
                score INTEGER,
                total_questions INTEGER,
                attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES onboarding_progress (employee_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_employee_record(self, slack_user_id: str, employee_name: str) -> str:
        """Create a new employee onboarding record."""
        employee_id = f"emp_{slack_user_id}_{int(datetime.now().timestamp())}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO onboarding_progress 
            (employee_id, slack_user_id, employee_name, start_date)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, slack_user_id, employee_name, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return employee_id
    
    def get_employee_progress(self, slack_user_id: str) -> Optional[Dict]:
        """Get employee progress by Slack user ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM onboarding_progress WHERE slack_user_id = ?
        ''', (slack_user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None
    
    def update_step_completion(self, slack_user_id: str, step: int, completed: bool = True, score: Optional[int] = None):
        """Update completion status for a specific step."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        step_column = f"step_{step}_"
        if step == 3:
            step_column += "history_quiz"
            cursor.execute(f'''
                UPDATE onboarding_progress 
                SET {step_column} = ?, last_activity = ?
                WHERE slack_user_id = ?
            ''', (score or 0, datetime.now(), slack_user_id))
        elif step == 4:
            step_column += "product_quiz"
            cursor.execute(f'''
                UPDATE onboarding_progress 
                SET {step_column} = ?, last_activity = ?
                WHERE slack_user_id = ?
            ''', (score or 0, datetime.now(), slack_user_id))
        else:
            step_mapping = {
                1: "github",
                2: "environment", 
                5: "team_integration",
                6: "technical_setup",
                7: "app_testing",
                8: "first_contribution"
            }
            step_column += step_mapping[step]
            cursor.execute(f'''
                UPDATE onboarding_progress 
                SET {step_column} = ?, last_activity = ?
                WHERE slack_user_id = ?
            ''', (completed, datetime.now(), slack_user_id))
        
        self._update_progress_metrics(cursor, slack_user_id)
        
        conn.commit()
        conn.close()
    
    def _update_progress_metrics(self, cursor, slack_user_id: str):
        """Update current step and completion percentage."""
        cursor.execute('''
            SELECT step_1_github, step_2_environment, step_3_history_quiz, 
                   step_4_product_quiz, step_5_team_integration, step_6_technical_setup,
                   step_7_app_testing, step_8_first_contribution
            FROM onboarding_progress WHERE slack_user_id = ?
        ''', (slack_user_id,))
        
        result = cursor.fetchone()
        if not result:
            return
        
        completed_steps = 0
        total_steps = 8
        
        boolean_steps = [result[0], result[1], result[4], result[5], result[6], result[7]]
        completed_steps += sum(boolean_steps)
        
        if result[2] >= 3:  # History quiz: 3/4 = 75%
            completed_steps += 1
        if result[3] >= 3:  # Product quiz: 3/3 = 100% (but we'll accept 2/3 = 67%)
            completed_steps += 1
        
        completion_percentage = (completed_steps / total_steps) * 100
        
        current_step = 1
        for i, step_completed in enumerate([
            result[0], result[1], result[2] >= 3, result[3] >= 2,
            result[4], result[5], result[6], result[7]
        ]):
            if not step_completed:
                current_step = i + 1
                break
        else:
            current_step = 9  # All steps completed
        
        cursor.execute('''
            UPDATE onboarding_progress 
            SET current_step = ?, completion_percentage = ?
            WHERE slack_user_id = ?
        ''', (current_step, completion_percentage, slack_user_id))
        
        if completion_percentage == 100:
            cursor.execute('''
                UPDATE onboarding_progress 
                SET completed_date = ?
                WHERE slack_user_id = ? AND completed_date IS NULL
            ''', (datetime.now(), slack_user_id))

class KatbusOnboardingBot:
    def __init__(self):
        required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "SLACK_APP_TOKEN"]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                           f"Please check your .env file contains these tokens.")
        
        self.app = App(
            token=os.environ.get("SLACK_BOT_TOKEN"),
            signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
        )
        self.db = OnboardingDatabase()
        self.setup_handlers()
        
        self.onboarding_steps = {
            1: OnboardingStep(
                1, "Create GitHub Account 🚀",
                "Set up your GitHub account for code collaboration",
                [
                    "Go to GitHub.com and click 'Sign Up'",
                    "Choose a fun username (K-pop themed encouraged!)",
                    "Use your email address and create a strong password",
                    "Verify your email address",
                    "Share your GitHub username with me!"
                ],
                "manual"
            ),
            2: OnboardingStep(
                2, "Development Environment Setup 💻",
                "Install and configure your coding environment",
                [
                    "Download Visual Studio Code from code.visualstudio.com",
                    "Install VS Code following the setup wizard",
                    "Clone the repository using Git",
                    "Take a screenshot of VS Code with the project open",
                    "Share the screenshot to confirm setup!"
                ],
                "screenshot"
            ),
            3: OnboardingStep(
                3, "Learn Katbus History 📚",
                "Test your knowledge of our company background",
                [
                    "Read through the history.md file in the repository",
                    "Take the interactive quiz below",
                    "Score at least 75% to proceed to the next step"
                ],
                "quiz",
                required_score=3
            ),
            4: OnboardingStep(
                4, "Understand Our Product 🎮",
                "Learn about Katlib and our educational mission",
                [
                    "Read through the product.md file",
                    "Take the product knowledge quiz",
                    "Score at least 67% to proceed"
                ],
                "quiz",
                required_score=2
            ),
            5: OnboardingStep(
                5, "Join the Team 👥",
                "Add yourself to our team structure",
                [
                    "Open team_structure.md in VS Code",
                    "Add your information to the New Team Member section",
                    "Include your name, role, bio, and Slack handle",
                    "Save the file and confirm completion"
                ],
                "manual"
            ),
            6: OnboardingStep(
                6, "Install Requirements 🛠️",
                "Set up the technical dependencies",
                [
                    "Open Terminal in VS Code",
                    "Run: pip install -r requirements.txt",
                    "Wait for installation to complete",
                    "Confirm successful installation"
                ],
                "manual"
            ),
            7: OnboardingStep(
                7, "Run Katlib 🎯",
                "Test the application and play the game",
                [
                    "Open katlib_gui.py in VS Code",
                    "Click the Run button (play icon)",
                    "Play through the Mad Libs game",
                    "Take a screenshot of the completed story",
                    "Share your experience!"
                ],
                "screenshot"
            ),
            8: OnboardingStep(
                8, "First Contribution 🌟",
                "Make your first code contribution",
                [
                    "Make a small change to the game (add a word, change a color)",
                    "Use VS Code's Source Control to stage changes",
                    "Write a commit message describing your changes",
                    "Commit and sync changes to GitHub",
                    "Share your contribution details!"
                ],
                "manual"
            )
        }
        
        self.history_quiz = [
            QuizQuestion(
                "What year was Katbus founded?",
                ["2020", "2021", "2022", "2023"],
                1,
                "Katbus was founded in 2021 by Shay as a passion project!"
            ),
            QuizQuestion(
                "What inspired the name 'Katbus'?",
                ["A cat riding a bus", "KATSEYE and Catbus from Studio Ghibli", "A keyboard shortcut", "A type of computer"],
                1,
                "The name combines KATSEYE (K-pop group) and Catbus (Studio Ghibli character)!"
            ),
            QuizQuestion(
                "How many team members does Katbus have today?",
                ["4", "5", "6", "7"],
                3,
                "Katbus has grown to a team of 7 passionate individuals!"
            ),
            QuizQuestion(
                "What was the first version of Katlib?",
                ["A web app", "A mobile game", "A Python Mad Libs game", "A board game"],
                2,
                "Katlib started as a simple Python Mad Libs game!"
            )
        ]
        
        self.product_quiz = [
            QuizQuestion(
                "What is the main goal of Katlib?",
                ["To teach math", "To make coding fun through storytelling", "To create music", "To design websites"],
                1,
                "Katlib makes coding education engaging through K-pop storytelling!"
            ),
            QuizQuestion(
                "What programming language is Katlib written in?",
                ["JavaScript", "Python", "Java", "C++"],
                1,
                "Katlib is built with Python for educational accessibility!"
            ),
            QuizQuestion(
                "What makes Katlib special?",
                ["It's free", "It combines K-pop with coding", "It's only for kids", "It's very fast"],
                1,
                "The unique combination of K-pop culture and coding education makes Katlib special!"
            )
        ]
    
    def setup_handlers(self):
        """Set up Slack event handlers."""
        
        @self.app.command("/onboard")
        def handle_onboard_command(ack, respond, command):
            ack()
            user_id = command['user_id']
            text = command.get('text', '').strip()
            
            if text.startswith('<@') and text.endswith('>'):
                target_user_id = text[2:-1].split('|')[0]
                self.start_onboarding(respond, target_user_id)
            else:
                self.start_onboarding(respond, user_id)
        
        @self.app.command("/progress")
        def handle_progress_command(ack, respond, command):
            ack()
            user_id = command['user_id']
            text = command.get('text', '').strip()
            
            if text.startswith('<@') and text.endswith('>'):
                target_user_id = text[2:-1].split('|')[0]
                self.show_progress(respond, target_user_id)
            else:
                self.show_progress(respond, user_id)
        
        @self.app.command("/dashboard")
        def handle_dashboard_command(ack, respond, command):
            ack()
            self.show_dashboard(respond)
        
        @self.app.action("quiz_answer")
        def handle_quiz_answer(ack, body, respond):
            ack()
            self.handle_quiz_answer_action(body, respond)
        
        @self.app.action("complete_step")
        def handle_step_completion(ack, body, respond):
            ack()
            self.complete_step(body, respond)
        
        @self.app.action("next_step")
        def handle_next_step(ack, body, respond):
            ack()
            self.show_next_step(body, respond)
    
    def start_onboarding(self, respond, user_id: str):
        """Start the onboarding process for a user."""
        try:
            client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
            user_info = client.users_info(user=user_id)
            user_name = user_info['user']['real_name'] or user_info['user']['name']
            
            progress = self.db.get_employee_progress(user_id)
            if not progress:
                self.db.create_employee_record(user_id, user_name)
                logger.info(f"Started onboarding for {user_name} ({user_id})")
            
            self.send_welcome_message(respond, user_name)
            self.show_current_step(respond, user_id)
            
        except SlackApiError as e:
            logger.error(f"Error starting onboarding: {e}")
            respond("Sorry, I encountered an error starting your onboarding. Please try again!")
    
    def send_welcome_message(self, respond, user_name: str):
        """Send personalized welcome message."""
        welcome_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Welcome to Katbus, {user_name}! 🎵✨"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Get ready for an amazing coding journey!* 🚀\n\nI'm your onboarding guide, and I'll help you through our 8-step process to become a full Katbus team member. Each step is designed to be fun and engaging - just like a K-pop concert! 🎤"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*What you'll accomplish:*\n• Set up your development environment 💻\n• Learn our company history and mission 📚\n• Master our product knowledge 🎮\n• Join our amazing team 👥\n• Make your first contribution 🌟"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "I'll track your progress and celebrate each milestone with you. Ready to start? Let's make coding as exciting as a K-pop concert! 🎊"
                }
            }
        ]
        
        respond(blocks=welcome_blocks)
    
    def show_current_step(self, respond, user_id: str):
        """Show the current onboarding step for a user."""
        progress = self.db.get_employee_progress(user_id)
        if not progress:
            respond("Please start your onboarding first with `/onboard`")
            return
        
        current_step = progress['current_step']
        if current_step > 8:
            self.show_completion_message(respond, progress)
            return
        
        step = self.onboarding_steps[current_step]
        completion_pct = progress['completion_percentage']
        
        step_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Step {step.step_number}: {step.title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Progress: {completion_pct:.0f}% Complete* 📊\n\n{step.description}"
                }
            }
        ]
        
        instructions_text = "\n".join([f"• {instruction}" for instruction in step.instructions])
        step_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Instructions:*\n{instructions_text}"
            }
        })
        
        if step.validation_type == "quiz":
            if current_step == 3:
                step_blocks.extend(self.create_quiz_blocks("history", self.history_quiz))
            elif current_step == 4:
                step_blocks.extend(self.create_quiz_blocks("product", self.product_quiz))
        else:
            step_blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "✅ Mark Complete"
                        },
                        "action_id": "complete_step",
                        "value": str(current_step),
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "❓ Need Help"
                        },
                        "action_id": "get_help",
                        "value": str(current_step)
                    }
                ]
            })
        
        respond(blocks=step_blocks)
    
    def create_quiz_blocks(self, quiz_type: str, questions: List[QuizQuestion]) -> List[Dict]:
        """Create interactive quiz blocks."""
        quiz_blocks = []
        
        for i, question in enumerate(questions):
            quiz_blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Question {i+1}:* {question.question}"
                }
            })
            
            options = []
            for j, option in enumerate(question.options):
                options.append({
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"{chr(65+j)}) {option}"
                    },
                    "action_id": "quiz_answer",
                    "value": f"{quiz_type}_{i}_{j}"
                })
            
            quiz_blocks.append({
                "type": "actions",
                "elements": options
            })
        
        return quiz_blocks
    
    def show_progress(self, respond, user_id: str):
        """Show detailed progress for a user."""
        progress = self.db.get_employee_progress(user_id)
        if not progress:
            respond("No onboarding record found. Please start with `/onboard`")
            return
        
        steps_status = []
        step_fields = [
            ('step_1_github', 'GitHub Account'),
            ('step_2_environment', 'Dev Environment'),
            ('step_3_history_quiz', 'History Quiz'),
            ('step_4_product_quiz', 'Product Quiz'),
            ('step_5_team_integration', 'Team Integration'),
            ('step_6_technical_setup', 'Technical Setup'),
            ('step_7_app_testing', 'App Testing'),
            ('step_8_first_contribution', 'First Contribution')
        ]
        
        for i, (field, name) in enumerate(step_fields, 1):
            value = progress[field]
            if field in ['step_3_history_quiz', 'step_4_product_quiz']:
                status = "✅" if value >= (3 if field == 'step_3_history_quiz' else 2) else f"📝 {value}/{'4' if field == 'step_3_history_quiz' else '3'}"
            else:
                status = "✅" if value else "⏳"
            
            steps_status.append(f"{i}. {name}: {status}")
        
        progress_text = "\n".join(steps_status)
        
        progress_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Onboarding Progress: {progress['completion_percentage']:.0f}%"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{progress['employee_name']}*\n\n{progress_text}"
                }
            }
        ]
        
        if progress['completion_percentage'] < 100:
            progress_blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Continue Onboarding"
                        },
                        "action_id": "next_step",
                        "style": "primary"
                    }
                ]
            })
        
        respond(blocks=progress_blocks)
    
    def show_dashboard(self, respond):
        """Show manager dashboard with all employee progress."""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT employee_name, completion_percentage, current_step, 
                   start_date, completed_date, last_activity
            FROM onboarding_progress
            ORDER BY start_date DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            respond("No onboarding records found.")
            return
        
        dashboard_text = "*Team Onboarding Dashboard* 📊\n\n"
        
        for name, completion, current_step, start_date, completed_date, last_activity in results:
            status = "✅ Complete" if completion == 100 else f"Step {current_step}/8"
            dashboard_text += f"• *{name}*: {completion:.0f}% - {status}\n"
        
        total_employees = len(results)
        completed_employees = sum(1 for r in results if r[1] == 100)
        avg_completion = sum(r[1] for r in results) / total_employees if total_employees > 0 else 0
        
        dashboard_text += "\n*Summary:*\n"
        dashboard_text += f"• Total Employees: {total_employees}\n"
        dashboard_text += f"• Completed: {completed_employees}\n"
        dashboard_text += f"• Average Progress: {avg_completion:.1f}%"
        
        respond(dashboard_text)
    
    def complete_step(self, body, respond):
        """Handle step completion."""
        user_id = body['user']['id']
        step_number = int(body['actions'][0]['value'])
        
        self.db.update_step_completion(user_id, step_number, True)
        
        celebrate_messages = [
            "🎉 Awesome job! You're making great progress!",
            "✨ Fantastic! You're one step closer to joining the team!",
            "🌟 Well done! Keep up the amazing work!",
            "🎊 Excellent! You're crushing this onboarding!",
            "💫 Great work! The team is excited to have you!"
        ]
        
        import random
        celebration = random.choice(celebrate_messages)
        respond(f"{celebration}\n\nStep {step_number} completed! Moving to the next step...")
        
        self.show_current_step(respond, user_id)
    
    def show_next_step(self, body, respond):
        """Show the next step in onboarding."""
        user_id = body['user']['id']
        self.show_current_step(respond, user_id)
    
    def handle_quiz_answer_action(self, body, respond):
        """Handle quiz answer selection."""
        user_id = body['user']['id']
        action_value = body['actions'][0]['value']
        
        parts = action_value.split('_')
        quiz_type = parts[0]
        question_index = int(parts[1])
        answer_index = int(parts[2])
        
        quiz_questions = self.history_quiz if quiz_type == 'history' else self.product_quiz
        question = quiz_questions[question_index]
        
        is_correct = answer_index == question.correct_answer
        
        if is_correct:
            respond(f"✅ Correct! {question.explanation}")
        else:
            correct_option = question.options[question.correct_answer]
            respond(f"❌ Not quite. The correct answer is: {correct_option}\n{question.explanation}")
        
        progress = self.db.get_employee_progress(user_id)
        if progress:
            current_step = progress['current_step']
            if current_step == 3 and quiz_type == 'history':
                self.db.update_step_completion(user_id, 3, True, 4)
                respond("🎉 History quiz completed! Moving to the next step...")
                self.show_current_step(respond, user_id)
            elif current_step == 4 and quiz_type == 'product':
                self.db.update_step_completion(user_id, 4, True, 3)
                respond("🎉 Product quiz completed! Moving to the next step...")
                self.show_current_step(respond, user_id)

    def show_completion_message(self, respond, progress):
        """Show completion celebration message."""
        completion_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🎉 Congratulations! Onboarding Complete! 🎉"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Amazing work, {progress['employee_name']}!* 🌟\n\nYou've successfully completed all 8 steps of the Katbus onboarding process. Welcome to the team! 🎵\n\n*What's next?*\n• Join our team channels\n• Start contributing to projects\n• Attend team meetings\n• Keep learning and growing with us!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The entire team is excited to work with you. Let's make coding as exciting as a K-pop concert! 🎤✨"
                }
            }
        ]
        
        respond(blocks=completion_blocks)
    
    def run(self):
        """Start the Slack bot."""
        handler = SocketModeHandler(self.app, os.environ["SLACK_APP_TOKEN"])
        handler.start()

if __name__ == "__main__":
    bot = KatbusOnboardingBot()
    bot.run()
