# Smart Email Reminder System

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)](https://developers.google.com/gmail/api)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-orange.svg)](https://spacy.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent email reminder system with a beautiful web interface that uses AI/NLP to automatically scan Gmail inboxes, identify deadlines, meetings, and other actionable events, and send email notifications for urgent items.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Web Dashboard](#web-dashboard)
- [Project Structure](#project-structure)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Smart Email Reminder System is a modern web application built with Streamlit that uses natural language processing to scan Gmail inboxes and identify important events like deadlines and meetings. It features a multi-page navigation interface with AI-powered event detection and automatic email notifications for urgent items.

### Key Capabilities

- **🎨 Beautiful Web Interface**: Modern multi-page Streamlit dashboard with dark theme
- **🤖 AI-Powered Event Detection**: Uses spaCy NER for intelligent temporal expression recognition
- **📧 Email Notifications**: Automatic email alerts for urgent and important events
- **🔒 Secure Authentication**: OAuth 2.0 with Google for safe Gmail access
- **📊 Visual Analytics**: Interactive dashboard with event statistics and urgency indicators
- **⚡ Real-time Processing**: Fast email scanning with smart filtering

## Features

### 🌐 Multi-Page Web Dashboard
- **Home**: Beautiful landing page with feature showcase
- **Authenticate**: Secure OAuth 2.0 Google login
- **Scan**: Configure and execute inbox analysis with progress tracking
- **Results**: Visual event display with urgency color-coding and statistics

### 🧠 Advanced NLP Processing
- spaCy-based Named Entity Recognition for dates, times, and events
- Context-aware date parsing supporting natural language
- Intelligent urgency classification (urgent/medium/low)
- Smart duplicate detection and event deduplication

### 📧 Email Notification System
- Automatic email alerts for urgent and important events
- Configurable notification preferences
- Beautiful email formatting with event summaries
- SMTP-based delivery with Gmail integration

### 🎨 Modern User Experience
- Clean, intuitive navigation flow
- Dark theme with gradient accents
- Responsive cards and statistics
- Real-time progress indicators
- Mobile-friendly design

### 🔐 Enterprise-Grade Security
- OAuth 2.0 token-based authentication
- Secure credential storage with environment variables
- No sensitive data in application code
- Automatic token refresh and session management

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 500MB free space

### Google Cloud Setup
1. **Google Cloud Project**: Create a new project at [Google Cloud Console](https://console.cloud.google.com/)
2. **Gmail API**: Enable the Gmail API for your project
3. **OAuth Credentials**: Create OAuth 2.0 Desktop Application credentials
4. **Download Credentials**: Save `credentials.json` to project root

### Python Dependencies
```bash
# Web Framework
streamlit>=1.28.0

# Google API
google-api-python-client>=2.0.0
google-auth-httplib2>=0.1.0
google-auth-oauthlib>=1.0.0

# NLP & Processing
spacy>=3.7.0
dateparser>=1.1.0

# Utilities
python-dotenv>=1.0.0
plyer>=2.1.0

# spaCy language model
en-core-web-sm>=3.7.0
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yaswanthsetty/NLP_Project_Email_Remainder.git
cd NLP_Project_Email_Remainder
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials (see Configuration section)
```

## Configuration

### Gmail API Setup
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API in the API Library
4. Create OAuth 2.0 credentials (Desktop Application)
5. Download `credentials.json` and place in project root

### Environment Variables
Create a `.env` file with the following configuration:

```env
# Gmail SMTP Configuration (Required for email notifications)
SENDER_EMAIL=your_gmail@gmail.com
SENDER_APP_PASSWORD=your_16_digit_app_password

# Optional: Test email recipient
TEST_EMAIL=test_recipient@example.com

# Optional: Default reminder email (if different from sender)
REMINDER_EMAIL=your_reminder_email@gmail.com
```

### Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a 16-digit app password for "Mail"
4. Use this password in the `SENDER_APP_PASSWORD` field

## Usage

### Web Dashboard (Recommended)
Launch the beautiful Streamlit web interface:

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501` in your browser.

### Dashboard Navigation Flow

1. **🏠 Home Page**: 
   - Welcome screen with feature overview
   - Click "Start Scanning" to begin

2. **🔐 Authenticate Page**:
   - Secure OAuth 2.0 Google login
   - One-time authentication (credentials cached)
   - Displays your authenticated email

3. **🔍 Scan Page**:
   - Configure time range (1, 3, 7, 14, or 30 days)
   - Set maximum emails to scan (10-100)
   - Enable/disable email notifications for urgent items
   - Real-time progress tracking
   - Automatic email notification for urgent events

4. **📊 Results Page**:
   - Visual statistics dashboard
   - Color-coded event cards (🚨 Urgent, ⚠️ Medium, 📅 Low)
   - Event details with dates and source emails
   - Options to scan again or logout

### Command Line Version
For automated/scheduled scans:

```bash
# Single scan
python main.py --once

# Continuous monitoring
python main.py
```

### First Run
On first execution, the system will:
1. Open browser for Gmail OAuth authentication
2. Request permission to access your Gmail account (read-only)
3. Generate and store access tokens locally in `token.json`
4. Begin processing your emails

## Web Dashboard

### Interface Features

🎨 **Modern Design**
- Clean dark theme with gradient accents
- Responsive layout for all screen sizes
- Intuitive navigation flow
- No sidebar - pure page-based navigation

📊 **Event Visualization**
- Color-coded urgency indicators:
  - 🚨 **Red**: Urgent (≤1 day or overdue)
  - ⚠️ **Orange**: Medium (2-7 days)
  - 📅 **Green**: Low (8+ days)
- Event statistics dashboard
- Source email tracking

🔔 **Smart Notifications**
- Automatic email alerts for urgent/important events
- Configurable notification preferences
- Beautiful email formatting with event summaries
- Sent to your authenticated Gmail address

### Dashboard Screenshots
The dashboard features:
- Hero section with feature cards
- Progress tracking during scans
- Beautiful event cards with context
- Statistics overview (Total, Urgent, Medium, Upcoming)

## Project Structure

```
NLP_Project_Email_Remainder/
├── app.py                      # Main Streamlit web dashboard
├── main.py                     # CLI version (optional)
├── auth.py                     # Gmail OAuth authentication
├── email_fetcher.py            # Email retrieval from Gmail API
├── email_parser.py             # Email parsing and text extraction
├── intelligence_module.py      # NLP event detection engine
├── notifier.py                 # Email notification system
├── check_setup.py              # Environment verification script
├── credentials.json            # Google OAuth credentials (create this)
├── token.json                  # OAuth tokens (auto-generated)
├── .env                        # Environment variables (create this)
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Core Modules

- **`app.py`**: Multi-page Streamlit dashboard with navigation (Home → Authenticate → Scan → Results)
- **`intelligence_module.py`**: spaCy-based NLP for event detection and urgency classification
- **`notifier.py`**: Email notification system with SMTP integration
- **`email_fetcher.py`**: Gmail API integration with server-side filtering
- **`email_parser.py`**: Robust MIME parsing for complex email formats
- **`auth.py`**: OAuth 2.0 authentication and token management

## Security

### Credential Management
- OAuth 2.0 tokens are stored locally and automatically refreshed
- Sensitive files (`credentials.json`, `token.json`) are excluded from version control
- Environment variables used for email notification configuration
- No hardcoded passwords or API keys in source code

### Best Practices
- Use Gmail App Passwords for SMTP (never use main account password)
- Keep `credentials.json` secure and never commit to repositories
- Regularly review OAuth permissions in Google Account settings
- Monitor API usage in Google Cloud Console

### Privacy
- All email processing happens locally on your machine
- No data is sent to external servers (except Google's Gmail API)
- Email content is never stored permanently
- Only temporary analysis for event detection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/NLP_Project_Email_Remainder.git
cd NLP_Project_Email_Remainder

# Create feature branch
git checkout -b feature/your-feature-name

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Make your changes and test thoroughly
streamlit run app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Streamlit** for the amazing web framework
- **Google Gmail API** for email access capabilities
- **spaCy** for advanced natural language processing
- **dateparser** for robust date and time parsing

---

**Built with ❤️ using Python, Streamlit, Google APIs, and modern NLP**

*Never miss another deadline hiding in your inbox!*