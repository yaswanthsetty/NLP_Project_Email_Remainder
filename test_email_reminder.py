#!/usr/bin/env python3
"""
Email Reminder Test Script for Smart Email Reminder System

This script tests the email reminder functionality to ensure it works properly.
"""

import os
import sys
from dotenv import load_dotenv
from notifier import send_email_reminder

def test_email_reminder():
    """Test the email reminder functionality."""

    print("📧 Smart Email Reminder - Email Test")
    print("=" * 50)

    # Load environment variables
    load_dotenv()

    # Check if required environment variables are set
    sender_email = os.getenv("SENDER_EMAIL")
    sender_app_password = os.getenv("SENDER_APP_PASSWORD")

    if not sender_email:
        print("❌ SENDER_EMAIL not found in .env file")
        print("💡 Please set SENDER_EMAIL=your_gmail@gmail.com in your .env file")
        return False

    if not sender_app_password:
        print("❌ SENDER_APP_PASSWORD not found in .env file")
        print("💡 Please set SENDER_APP_PASSWORD=your_16_digit_app_password in your .env file")
        print("💡 Generate an App Password at: https://myaccount.google.com/apppasswords")
        return False

    print(f"Sender Email: {sender_email}")
    print("App Password: [HIDDEN]")
    print()

    # Test email content
    test_subject = "🔔 Test Reminder - Smart Email System"
    test_body = """🔔 Smart Email Reminder Test

📅 Test Meeting Reminder

📝 This is a test reminder to verify that your email notification system is working properly.

📧 Original Email Subject: Test Email
👤 From: Smart Email Reminder System
🕒 Detected: System Test

---
This is an automated test reminder from the Smart Email Reminder System.
If you received this email, your email notification setup is working correctly!
"""

    print("Sending test email reminder...")
    success = send_email_reminder(sender_email, test_subject, test_body)

    if success:
        print("✅ Email reminder test completed successfully!")
        print(f"📧 Check your inbox at {sender_email} for the test reminder")
        return True
    else:
        print("❌ Email reminder test failed")
        print("💡 Check your Gmail App Password and internet connection")
        return False

if __name__ == "__main__":
    test_email_reminder()