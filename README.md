# Smart Email Reminder System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)](https://developers.google.com/gmail/api)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-orange.svg)](https://spacy.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent email reminder system that uses natural language processing to automatically scan Gmail inboxes, identify deadlines, meetings, and other actionable events, and send timely desktop notifications.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security](#security)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Smart Email Reminder System is a Python application that uses natural language processing to scan Gmail inboxes and identify important events like deadlines and meetings. It automatically sends desktop notifications to help users stay on top of their schedule.

### Key Capabilities

- **Intelligent Event Detection**: Uses spaCy NER and dateparser for robust temporal expression recognition
- **Real-time Email Processing**: Continuously monitors Gmail inbox with configurable intervals
- **Cross-platform Notifications**: Native desktop notifications with fallback mechanisms
- **Enterprise Security**: OAuth 2.0 authentication with secure credential management
- **Modular Architecture**: Clean separation of concerns for maintainability and extensibility

## Architecture

The system implements a modular, microservices-inspired architecture with five core components:

### 1. Authentication Module (`auth.py`)
- OAuth 2.0 flow implementation for Gmail API access
- Secure token management and refresh logic
- Credential validation and error handling

### 2. Email Ingestion Module (`email_fetcher.py`)
- Server-side email filtering using Gmail search queries
- Efficient API usage with pagination support
- Raw email content retrieval and metadata extraction

### 3. Content Processing Module (`email_parser.py`)
- Robust email parsing for complex MIME structures
- Header decoding and character encoding handling
- Clean text extraction from multipart messages

### 4. Intelligence Engine (`intelligence_module.py`)
- spaCy-powered Named Entity Recognition for temporal expressions
- Advanced date parsing with context awareness
- Actionable event classification and prioritization

### 5. Notification System (`notifier.py`)
- Cross-platform desktop notification delivery
- Windows toast notification support with PowerShell integration
- Email notification fallback mechanisms

### 6. Orchestration Layer (`main.py`)
- Workflow coordination and scheduling
- Error handling and recovery mechanisms
- Continuous operation with configurable intervals

## Features

### Autonomous Operation
- Continuous background monitoring with configurable intervals
- Zero manual intervention required after initial setup
- Intelligent duplicate detection and notification throttling

### Advanced NLP Processing
- spaCy-based Named Entity Recognition for temporal expressions
- Context-aware date parsing with multiple format support
- Intelligent event classification and urgency assessment

### Comprehensive Email Analysis
- Support for complex email formats (HTML, plain text, multipart)
- Header decoding for international character sets
- Subject line and body content integration

### Intelligent Notifications
- Native desktop notifications with rich formatting
- Windows-specific toast notifications with PowerShell integration
- Console fallback for guaranteed visibility
- Configurable notification urgency levels

### Enterprise-Grade Security
- OAuth 2.0 token-based authentication
- Secure credential storage with environment variables
- No sensitive data in application code
- Automatic token refresh and session management

### Performance Optimized
- Server-side email filtering to minimize API calls
- Efficient text processing with caching mechanisms
- Background operation with minimal system resource usage

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
# Core dependencies
google-api-python-client==2.0.0
google-auth-httplib2==0.1.0
google-auth-oauthlib==1.0.0
spacy==3.7.0
dateparser==1.1.0
plyer==2.1.0
python-dotenv==1.0.0
schedule==1.2.0

# spaCy language model
en-core-web-sm==3.7.0
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

### Quick Start
```bash
# Run complete system with continuous monitoring
python main.py

# Run single execution (recommended for cron jobs)
python main.py --once
```

### Command Line Options
```bash
python main.py              # Continuous mode with 15-minute intervals
python main.py --once       # Single execution mode
python main.py --help       # Display help information
```

### First Run
On first execution, the system will:
1. Open browser for Gmail OAuth authentication
2. Request permission to access your Gmail account
3. Generate and store access tokens locally
4. Begin monitoring for new emails

## Testing

### Automated Testing
```bash
# Run notification tests
python test_notifications.py

# Send test email with sample events
python send_test_email.py
```

### Manual Testing
1. **Send Test Email**:
   ```bash
   python send_test_email.py
   ```

2. **Run Detection**:
   ```bash
   python main.py --once
   ```

3. **Expected Results**: The system should detect events such as:
   - **Q3 Financial Report**: Due next Friday
   - **Client Presentation**: October 28th at 2 PM PST
   - **Team Standup**: Next Tuesday at 10 AM EST
   - **Budget Review**: Next Wednesday at 3 PM EST
   - **Project Kickoff**: December 15th at 11 AM EST
   - **Code Review**: 25th of current month
   - **Training Session**: Next Monday at 9 AM EST

## Deployment

### Production Recommendations

#### Linux/macOS (Cron)
```bash
# Edit crontab
crontab -e

# Add line for 15-minute intervals
*/15 * * * * cd /path/to/project && python3 main.py --once >> cron.log 2>&1

# Alternative: Hourly execution
0 * * * * cd /path/to/project && python3 main.py --once >> cron.log 2>&1
```

#### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create new task with these settings:
   - **Program**: `python.exe`
   - **Arguments**: `main.py --once`
   - **Start in**: `D:\Path\To\Your\Project`
   - **Trigger**: Daily, every 15 minutes

#### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
CMD ["python", "main.py", "--once"]
```

## Security

### Credential Management
- OAuth 2.0 tokens are stored locally and automatically refreshed
- Sensitive files (`credentials.json`, `token.json`) are excluded from version control
- Environment variables used for configuration
- No hardcoded passwords or API keys

### Best Practices
- Regularly rotate OAuth tokens
- Use app passwords instead of main account passwords
- Keep credentials.json secure and never commit to repositories
- Monitor API usage in Google Cloud Console

## Project Structure

```
NLP_Project_Email_Remainder/
├── � auth.py                 # Gmail OAuth 2.0 authentication
├── 📄 email_fetcher.py        # Email search and retrieval
├── 📄 email_parser.py         # Email content parsing
├── 📄 intelligence_module.py  # NLP event detection
├── 📄 notifier.py            # Notification system
├── 📄 main.py                # Main orchestration
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env.example          # Environment template
├── � .gitignore            # Git ignore rules
└── 📄 README.md             # Project documentation
```

## � Contributing

This project demonstrates modern Python development practices with:
- Modular architecture and clean code principles
- Comprehensive error handling and logging
- Type hints and documentation
- Automated testing and validation

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/NLP_Project_Email_Remainder.git
cd NLP_Project_Email_Remainder

# Create feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Gmail API** for email access capabilities
- **spaCy** for advanced natural language processing
- **dateparser** for robust date and time parsing
- **plyer** for cross-platform notification support

---

**Built with ❤️ using Python, Google APIs, and modern NLP techniques**

*Developed by Yaswanth Setty - Intelligent Email Processing for the Modern Professional*