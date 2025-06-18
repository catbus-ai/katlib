# Katbus Slack Onboarding System Setup

## Overview
This system provides an interactive Slack-based onboarding experience for new Katbus employees, with real-time progress tracking and a web dashboard for managers.

## Components
1. **Slack Bot** (`slack_bot.py`) - Interactive onboarding guide
2. **Web Dashboard** (`dashboard.py`) - Manager progress tracking interface
3. **Database** - SQLite database for progress storage
4. **Templates** - HTML templates for the web dashboard

## Prerequisites
- Python 3.8+
- Slack workspace with admin access
- Slack app creation permissions

## Setup Instructions

### 1. Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "Katbus Onboarding Bot"
4. Select your workspace

### 2. Configure Slack App Permissions
**OAuth & Permissions:**
- `app_mentions:read`
- `channels:read`
- `chat:write`
- `commands`
- `users:read`
- `users:read.email`

**Slash Commands:**
- `/onboard` - Start onboarding process
- `/progress` - Check progress
- `/dashboard` - View manager dashboard

**Interactive Components:**
- Enable "Interactivity & Shortcuts"
- Request URL: `https://your-domain.com/slack/events`

### 3. Install Dependencies
```bash
pip install -r requirements_slack.txt
```

### 4. Environment Variables
Copy the example file and fill in your tokens:
```bash
cp .env.example .env
```

Then edit `.env` with your actual Slack app tokens:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
```

### 5. Quick Start (Recommended)
**Run the quick start checker:**
```bash
python quick_start.py
```

This will verify all prerequisites and guide you through any missing setup steps.

**Create demo data (optional):**
```bash
python demo_data.py
```

### 6. Run the System
**Start Slack Bot:**
```bash
python slack_bot.py
```

**Start Web Dashboard:**
```bash
python dashboard.py
```

The dashboard will be available at `http://localhost:5000`

## Usage

### For New Employees
1. Manager runs `/onboard @username` in Slack
2. Bot sends welcome message and starts Step 1
3. Employee follows interactive prompts
4. Bot tracks progress and provides guidance
5. Celebrates completion milestones

### For Managers
1. Access web dashboard at configured URL
2. View real-time progress for all employees
3. See completion percentages and bottlenecks
4. Monitor quiz scores and step completion
5. Send reminders or encouragement

## Features

### Interactive Onboarding Steps
1. **GitHub Account Setup** - Guided account creation
2. **Development Environment** - VS Code installation and setup
3. **Company History Quiz** - Interactive knowledge test
4. **Product Knowledge Quiz** - Understanding Katlib
5. **Team Integration** - Adding to team structure
6. **Technical Setup** - Dependencies installation
7. **Application Testing** - Running and testing Katlib
8. **First Contribution** - Making initial code changes

### Progress Tracking
- Real-time completion percentages
- Step-by-step status indicators
- Quiz score tracking
- Time-based analytics
- Automated milestone celebrations

### Manager Dashboard
- Multi-employee progress overview
- Completion rate analytics
- Step-specific bottleneck identification
- Daily onboarding start tracking
- Individual employee detail views

## Database Schema
The system uses SQLite with two main tables:
- `onboarding_progress` - Employee progress tracking
- `quiz_attempts` - Quiz attempt history

## Customization

### Adding New Steps
1. Update `onboarding_steps` dictionary in `slack_bot.py`
2. Add corresponding database fields
3. Implement validation logic
4. Update dashboard templates

### Modifying Quizzes
1. Edit `history_quiz` and `product_quiz` arrays
2. Update scoring thresholds
3. Add new quiz types as needed

### Dashboard Styling
1. Modify HTML templates in `templates/`
2. Update CSS styles
3. Add new chart types using Plotly

## Security Considerations
- Store Slack tokens securely
- Implement proper access controls
- Regular database backups
- Monitor for unauthorized access
- Follow Slack security best practices

## Troubleshooting

### Common Issues
1. **Bot not responding**: Check token permissions
2. **Database errors**: Verify SQLite file permissions
3. **Dashboard not loading**: Check Flask dependencies
4. **Quiz not working**: Verify interactive components setup

### Logs
- Bot logs: Check console output
- Dashboard logs: Flask debug mode
- Database logs: SQLite error messages

## Support
For technical support or feature requests, contact the development team or create an issue in the repository.
