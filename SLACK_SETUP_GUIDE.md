# 🚀 Slack App Setup Guide - Step by Step

## What You Need to Do vs What the System Does

**👤 YOU DO:** Create Slack app, get 3 tokens, paste them in .env file (5 minutes)  
**🤖 SYSTEM DOES:** Everything else automatically (bot responses, progress tracking, dashboard)

---

## Step 1: Create Your Slack App (2 minutes)

### 1.1 Go to Slack API Website
- Open your browser and go to: **https://api.slack.com/apps**
- Click the green **"Create New App"** button

### 1.2 Choose App Creation Method
- Select **"From scratch"** (not "From app manifest")
- App Name: **`Katbus Onboarding Bot`**
- Pick your workspace from the dropdown
- Click **"Create App"**

---

## Step 2: Configure App Permissions (2 minutes)

### 2.1 Set OAuth Permissions
- In your new app, click **"OAuth & Permissions"** in the left sidebar
- Scroll down to **"Scopes"** section
- Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"** and add these 6 permissions:
  - `app_mentions:read`
  - `channels:read`
  - `chat:write`
  - `commands`
  - `users:read`
  - `users:read.email`

### 2.2 Install App to Workspace
- Scroll to top of OAuth & Permissions page
- Click **"Install to Workspace"**
- Click **"Allow"** when prompted
- **COPY THE BOT TOKEN** (starts with `xoxb-`) - you'll need this!

---

## Step 3: Enable Socket Mode (1 minute)

### 3.1 Turn On Socket Mode
- Click **"Socket Mode"** in left sidebar
- Toggle **"Enable Socket Mode"** to ON
- App Name: **`Katbus Onboarding Bot`**
- Click **"Generate"** to create app-level token
- **COPY THE APP TOKEN** (starts with `xapp-`) - you'll need this!

### 3.2 Get Signing Secret
- Click **"Basic Information"** in left sidebar
- Under **"App Credentials"**, find **"Signing Secret"**
- Click **"Show"** and **COPY THE SIGNING SECRET** - you'll need this!

---

## Step 4: Create Slash Commands (1 minute)

### 4.1 Add Commands
- Click **"Slash Commands"** in left sidebar
- Click **"Create New Command"** and add these 3 commands:

**Command 1:**
- Command: `/onboard`
- Description: `Start onboarding for a new employee`
- Click **"Save"**

**Command 2:**
- Command: `/progress`
- Description: `Check onboarding progress`
- Click **"Save"**

**Command 3:**
- Command: `/dashboard`
- Description: `View manager dashboard`
- Click **"Save"**

---

## Step 5: Set Up Environment File (30 seconds)

### 5.1 Create Your .env File
In your katlib folder, copy the example file:
```bash
cp .env.example .env
```

### 5.2 Add Your 3 Tokens
Edit the `.env` file and replace the placeholder values with your actual tokens:

```bash
SLACK_BOT_TOKEN=xoxb-your-actual-bot-token-from-step-2
SLACK_SIGNING_SECRET=your-actual-signing-secret-from-step-3
SLACK_APP_TOKEN=xapp-your-actual-app-token-from-step-3
```

---

## Step 6: Test Everything Works

### 6.1 Run the Quick Check
```bash
python quick_start.py
```

You should see all green checkmarks ✅

### 6.2 Start the System
**Terminal 1 - Start Bot:**
```bash
python slack_bot.py
```

**Terminal 2 - Start Dashboard:**
```bash
python dashboard.py
```

### 6.3 Test in Slack
In any Slack channel, type:
```
/onboard @tempest
```

The bot should respond with a welcome message! 🎉

---

## 🎯 What Happens After Setup

1. **For Tempest:** She gets guided through 8 steps automatically
2. **For You:** Track her progress at the dashboard URL
3. **System handles:** All interactions, quizzes, progress tracking, celebrations

## 🆘 If Something Goes Wrong

**Bot doesn't respond?**
- Check your tokens are correct in .env file
- Make sure both python processes are running

**Commands not working?**
- Reinstall the app to your workspace in OAuth & Permissions

**Need help?**
- Run: `python quick_start.py --slack-setup`
- Check the console output for error messages

---

## 🎉 You're Done!

Once setup is complete, the system runs itself. Just use `/onboard @username` to start anyone's onboarding journey!
