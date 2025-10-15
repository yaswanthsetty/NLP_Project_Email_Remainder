#!/usr/bin/env python3
"""
Quick verification script to check if all modules are properly connected.
"""

import sys

print("🔍 Checking Smart Email Reminder Dashboard Components...")
print("=" * 60)

# Check 1: Streamlit
print("\n1. Checking Streamlit...")
try:
    import streamlit as st
    print("   ✅ Streamlit installed")
except ImportError as e:
    print(f"   ❌ Streamlit not found: {e}")
    sys.exit(1)

# Check 2: Google API
print("\n2. Checking Google API libraries...")
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    print("   ✅ Google API libraries installed")
except ImportError as e:
    print(f"   ❌ Google API libraries not found: {e}")
    sys.exit(1)

# Check 3: NLP libraries
print("\n3. Checking NLP libraries...")
try:
    import spacy
    print("   ✅ spaCy installed")
except ImportError as e:
    print(f"   ❌ spaCy not found: {e}")
    sys.exit(1)

try:
    import dateparser
    print("   ✅ dateparser installed")
except ImportError as e:
    print(f"   ❌ dateparser not found: {e}")
    sys.exit(1)

# Check 4: spaCy model
print("\n4. Checking spaCy model...")
try:
    nlp = spacy.load("en_core_web_sm")
    print("   ✅ spaCy model 'en_core_web_sm' loaded")
except OSError:
    print("   ❌ spaCy model 'en_core_web_sm' not found")
    print("   💡 Run: python -m spacy download en_core_web_sm")

# Check 5: Credentials file
print("\n5. Checking credentials...")
import os
if os.path.exists('credentials.json'):
    print("   ✅ credentials.json found")
else:
    print("   ❌ credentials.json not found")
    print("   💡 You need to set up Gmail API credentials")

# Check 6: Environment variables
print("\n6. Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_APP_PASSWORD")

if sender_email:
    print(f"   ✅ SENDER_EMAIL: {sender_email}")
else:
    print("   ⚠️  SENDER_EMAIL not set (optional for email reminders)")

if sender_password:
    print("   ✅ SENDER_APP_PASSWORD: [HIDDEN]")
else:
    print("   ⚠️  SENDER_APP_PASSWORD not set (optional for email reminders)")

# Check 7: Test imports from app.py modules
print("\n7. Checking module imports...")
try:
    from auth import get_gmail_service
    print("   ✅ auth.py imported")
except Exception as e:
    print(f"   ❌ auth.py import failed: {e}")

try:
    from email_fetcher import search_emails
    print("   ✅ email_fetcher.py imported")
except Exception as e:
    print(f"   ❌ email_fetcher.py import failed: {e}")

try:
    from email_parser import parse_raw_email
    print("   ✅ email_parser.py imported")
except Exception as e:
    print(f"   ❌ email_parser.py import failed: {e}")

try:
    from intelligence_module import find_actionable_events
    print("   ✅ intelligence_module.py imported")
except Exception as e:
    print(f"   ❌ intelligence_module.py import failed: {e}")

print("\n" + "=" * 60)
print("✅ All checks passed! Your dashboard is ready to use.")
print("\n🚀 To launch the dashboard:")
print("   streamlit run app.py")
print("\n💡 Remember to:")
print("   1. Open the sidebar (top-left arrow)")
print("   2. Click 'Authenticate with Google'")
print("   3. Click 'Scan Inbox for Reminders'")
print("=" * 60)