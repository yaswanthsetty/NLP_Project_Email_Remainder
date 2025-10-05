# Smart Email Reminder System

A Python-based intelligent email reminder system that autonomously scans Gmail inbox, identifies actionable information like deadlines or tasks, and generates timely reminders using Natural Language Processing.

## 🏗️ Architecture Overview

The system follows a modular design with five distinct components:

1. **Authentication & Authorization Module** (`auth.py`) - Securely connects to Gmail using OAuth 2.0
2. **Email Ingestion & Filtering Module** (`email_fetcher.py`) - Efficiently fetches relevant emails using server-side filtering
3. **Content Parsing & Extraction Module** - Processes raw email data into clean, analyzable text
4. **Intelligence & NLP Module** - Uses NLP to extract dates, times, and actionable events
5. **Notification & Scheduling Module** - Generates alerts and manages periodic workflow execution

## 📁 Project Structure

```
NLP_Project_Email_Remainder/
├── auth.py                    # Gmail OAuth 2.0 authentication
├── email_fetcher.py           # Email searching and raw content fetching
├── email_parser.py            # Email content parsing and text extraction
├── intelligence_module.py     # NLP-powered actionable event detection
├── notifier.py               # Desktop and email notification system
├── main.py                   # Main orchestration and scheduling script
├── test_email_fetcher.py     # Test suite for email fetcher module
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── .gitignore               # Git ignore rules (includes credentials protection)
└── README.md                # Project documentation
```

## 🚀 Current Status

### ✅ Completed Modules

- **Authentication & Authorization Module** (`auth.py`) - Complete OAuth 2.0 flow implementation
- **Email Ingestion & Filtering Module** (`email_fetcher.py`) - Server-side email filtering and raw content fetching
- **Content Parsing & Extraction Module** (`email_parser.py`) - Email content parsing and text extraction
- **Intelligence & NLP Module** (`intelligence_module.py`) - NLP-powered event detection and date parsing
- **Notification & Scheduling Module** (`notifier.py`, `main.py`) - Desktop notifications and workflow orchestration

### 🎯 System Status: **FULLY OPERATIONAL**

The Smart Email Reminder System is now complete and ready for deployment!

## 🛠️ Setup Instructions

### Prerequisites

1. **Google Cloud Project Setup:**
   - Create a Google Cloud Project
   - Enable the Gmail API
   - Create OAuth 2.0 Desktop Application credentials
   - Download `credentials.json`

2. **Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Environment Configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your email credentials (see Email Setup below)
   ```

### Email Setup (Optional - for email notifications)

1. **Enable 2FA on your Gmail account**
2. **Generate App Password:**
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Generate a 16-digit app password
3. **Configure .env file:**
   ```
   SENDER_EMAIL=your_gmail@gmail.com
   SENDER_APP_PASSWORD=your_16_digit_app_password
   ```

### Usage

1. **Quick Start - Run the Complete System:**
   ```bash
   python main.py
   ```

2. **Test Your System:**
   ```bash
   python send_test_email.py    # Send yourself a test email with events
   python main.py --once        # Run the system to detect events
   ```

3. **Single Run (for cron jobs):**
   ```bash
   python main.py --once
   ```

### Testing Your System

1. **Send a Test Email:**
   ```bash
   python send_test_email.py
   ```
   This sends you an email containing multiple deadlines and events that your system should detect.

2. **Run the System:**
   ```bash
   python main.py --once
   ```
   The system will scan unread emails and send desktop notifications for detected events.

3. **Expected Test Results:**
   Your system should detect these events from the test email:
   - **next Friday** - Q3 financial report deadline
   - **October 28th at 2 PM PST** - Client presentation
   - **next Tuesday at 10 AM EST** - Team standup meeting
   - **next Wednesday at 3 PM EST** - Budget review session
   - **December 15th at 11 AM EST** - Project kickoff
   - **the 25th of this month** - Code review deadline
   - **next Monday at 9 AM EST** - Training session

### Production Deployment

For production use, consider using system schedulers:

**Linux/macOS (cron):**
```bash
# Run every 15 minutes
*/15 * * * * cd /path/to/project && python3 main.py --once >> cron.log 2>&1
```

**Windows (Task Scheduler):**
- Program: `python`
- Arguments: `main.py --once`
- Start in: `D:\Path\To\Your\Project`

## 🔒 Security

- `credentials.json` and `token.json` are automatically excluded from version control
- OAuth 2.0 provides secure, token-based authentication
- No passwords or sensitive data stored in code

## 🎯 Key Features

- **🤖 Fully Autonomous Operation** - Runs continuously with configurable scheduling
- **🧠 Advanced NLP Processing** - Uses spaCy and dateparser for intelligent event detection
- **📧 Smart Email Analysis** - Parses complex email formats and extracts actionable content
- **🔔 Multi-Platform Notifications** - Desktop notifications with optional email alerts
- **🔒 Enterprise-Grade Security** - OAuth 2.0 with secure credential management
- **⚡ Efficient Processing** - Server-side filtering for optimal Gmail API usage
- **🏗️ Modular Architecture** - Clean separation of concerns for easy maintenance
- **🧪 Comprehensive Testing** - Full test coverage for reliable operation
- **📱 Cross-Platform Support** - Works on Windows, macOS, and Linux
- **⏰ Flexible Scheduling** - Built-in scheduler or system cron integration

## 🧪 Testing

The project includes comprehensive test suites for each module:
- Module structure validation
- Function signature verification
- Error handling validation
- Integration testing

## 📈 Future Enhancements

- Advanced NLP for context understanding
- Machine learning for improved deadline detection
- Multi-platform notification support
- Web dashboard for reminder management
- Email priority classification

## 🤝 Contributing

This is an educational project demonstrating modern Python development practices with Google APIs and NLP integration.

---

*Built with Python, Google Gmail API, and modern software engineering practices.*