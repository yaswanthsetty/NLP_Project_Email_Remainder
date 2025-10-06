#!/usr/bin/env python3
"""
Smart Email Reminder Dashboard - Streamlit Web Application

A beautiful, modern web interface for the Smart Email Reminder System.
Features dark theme, elegant UI, and real-time email scanning capabilities.

Required packages:
pip install streamlit google-api-python-client google-auth-httplib2 google-auth-oauthlib spacy dateparser plyer python-dotenv

Usage:
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import json
import os
import base64
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time

# Core imports for email processing
import email
import smtplib
from email.message import EmailMessage
from email.header import decode_header, make_header

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    st.error("⚠️ Google API libraries not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    st.stop()

# NLP imports
try:
    import spacy
    import dateparser
except ImportError:
    st.error("⚠️ NLP libraries not installed. Run: pip install spacy dateparser")
    st.stop()

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Smart Email Reminders",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================

def load_css():
    """Inject custom CSS for a stunning dark theme and modern aesthetics."""
    css = """
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #4ECDC4;
        --accent-color: #FF6B6B;
        --background-dark: #0E1117;
        --surface-dark: #1E2329;
        --surface-light: #262730;
        --text-primary: #FAFAFA;
        --text-secondary: #A0A0A0;
        --success-color: #00C851;
        --warning-color: #FFB347;
        --border-radius: 12px;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Overall app styling */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }
    
    /* Event card styling */
    .event-card {
        background: var(--surface-dark);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary-color);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .event-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-left-color: var(--secondary-color);
    }
    
    .event-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .event-date {
        font-size: 0.9rem;
        color: var(--secondary-color);
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .event-source {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-style: italic;
    }
    
    .event-urgency-high {
        border-left-color: var(--accent-color) !important;
    }
    
    .event-urgency-medium {
        border-left-color: var(--warning-color) !important;
    }
    
    .event-urgency-low {
        border-left-color: var(--success-color) !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: var(--surface-dark);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-hover);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: rgba(0, 200, 81, 0.1);
        border-left: 4px solid var(--success-color);
        border-radius: var(--border-radius);
    }
    
    .stError {
        background: rgba(255, 107, 107, 0.1);
        border-left: 4px solid var(--accent-color);
        border-radius: var(--border-radius);
    }
    
    .stInfo {
        background: rgba(108, 99, 255, 0.1);
        border-left: 4px solid var(--primary-color);
        border-radius: var(--border-radius);
    }
    
    /* Statistics cards */
    .stat-card {
        background: var(--surface-light);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# =============================================================================
# AUTHENTICATION MODULE
# =============================================================================

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """
    Authenticate and return Gmail service object using OAuth 2.0.
    Returns the service object and user's email address.
    """
    creds = None
    
    # Check if token.json exists (previous authentication)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials, request authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                st.error(f"Failed to refresh credentials: {e}")
                return None, None
        else:
            if not os.path.exists('credentials.json'):
                st.error("❌ credentials.json not found. Please set up Gmail API credentials.")
                return None, None
                
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                st.error(f"Authentication failed: {e}")
                return None, None
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Get user's email address
        profile = service.users().getProfile(userId='me').execute()
        user_email = profile.get('emailAddress', 'Unknown')
        
        return service, user_email
    except Exception as e:
        st.error(f"Failed to build Gmail service: {e}")
        return None, None

# =============================================================================
# EMAIL FETCHING MODULE
# =============================================================================

def search_emails(service, query: str = "is:unread newer_than:7d", max_results: int = 50):
    """
    Search for emails using Gmail API with specified query.
    """
    try:
        result = service.users().messages().list(
            userId='me', 
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = result.get('messages', [])
        return messages
        
    except HttpError as error:
        st.error(f"An error occurred while searching emails: {error}")
        return []

def get_raw_email(service, message_id: str):
    """
    Retrieve raw email content by message ID.
    """
    try:
        message = service.users().messages().get(
            userId='me', 
            id=message_id, 
            format='raw'
        ).execute()
        
        raw_email = base64.urlsafe_b64decode(
            message['raw'].encode('ASCII')
        )
        
        return raw_email
        
    except HttpError as error:
        st.error(f"An error occurred while fetching email {message_id}: {error}")
        return None

# =============================================================================
# EMAIL PARSING MODULE
# =============================================================================

def decode_email_header(header_string):
    """Handle potentially encoded email headers."""
    if not header_string:
        return ""
    
    try:
        decoded_parts = decode_header(header_string)
        decoded_header = make_header(decoded_parts)
        return str(decoded_header)
    except Exception as e:
        return str(header_string)

def get_email_body(email_message):
    """Extract clean plain text from email body."""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        return payload.decode(charset, errors='ignore')
                except Exception:
                    continue
    else:
        try:
            payload = email_message.get_payload(decode=True)
            if payload:
                charset = email_message.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='ignore')
        except Exception:
            pass
    
    return ""

def parse_raw_email(raw_email_bytes):
    """Parse raw email bytes into structured data."""
    if not raw_email_bytes:
        return {'subject': '', 'from': '', 'to': '', 'body': ''}
    
    try:
        email_message = email.message_from_bytes(raw_email_bytes)
        
        subject = decode_email_header(email_message.get('Subject', ''))
        from_address = decode_email_header(email_message.get('From', ''))
        to_address = decode_email_header(email_message.get('To', ''))
        body = get_email_body(email_message)
        
        return {
            'subject': subject,
            'from': from_address,
            'to': to_address,
            'body': body
        }
    except Exception as e:
        st.error(f"Error parsing email: {e}")
        return {'subject': '', 'from': '', 'to': '', 'body': ''}

# =============================================================================
# INTELLIGENCE MODULE
# =============================================================================

def load_nlp_model():
    """Load spaCy model with error handling."""
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        st.error("❌ spaCy model 'en_core_web_sm' not found. Please install it:")
        st.code("python -m spacy download en_core_web_sm")
        return None

def find_actionable_events(text: str) -> List[Dict[str, Any]]:
    """Analyze email text to identify actionable events."""
    if not text or not text.strip():
        return []
    
    nlp = load_nlp_model()
    if not nlp:
        return []
    
    try:
        doc = nlp(text)
        events = []
        
        # Look for date entities and surrounding context
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME", "EVENT"]:
                # Get surrounding context (10 words before and after)
                start = max(0, ent.start - 10)
                end = min(len(doc), ent.end + 10)
                context = doc[start:end].text
                
                # Try to parse the date
                parsed_date = dateparser.parse(ent.text)
                
                if parsed_date:
                    # Determine urgency based on time until event
                    days_until = (parsed_date - datetime.now()).days
                    
                    if days_until < 0:
                        urgency = "overdue"
                        urgency_color = "high"
                    elif days_until <= 1:
                        urgency = "urgent"
                        urgency_color = "high"
                    elif days_until <= 7:
                        urgency = "soon"
                        urgency_color = "medium"
                    else:
                        urgency = "upcoming"
                        urgency_color = "low"
                    
                    events.append({
                        'original_text': ent.text,
                        'context': context,
                        'parsed_date': parsed_date,
                        'days_until': days_until,
                        'urgency': urgency,
                        'urgency_color': urgency_color,
                        'formatted_date': parsed_date.strftime('%A, %B %d, %Y at %I:%M %p')
                    })
        
        # Sort events by date
        events.sort(key=lambda x: x['parsed_date'])
        return events
        
    except Exception as e:
        st.error(f"Error in NLP processing: {e}")
        return []

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_urgency_emoji(urgency_color: str) -> str:
    """Get emoji based on urgency level."""
    emoji_map = {
        "high": "🚨",
        "medium": "⚠️",
        "low": "📅"
    }
    return emoji_map.get(urgency_color, "📅")

def format_time_until(days_until: int) -> str:
    """Format time until event in human-readable form."""
    if days_until < 0:
        return f"{abs(days_until)} days overdue"
    elif days_until == 0:
        return "Today"
    elif days_until == 1:
        return "Tomorrow"
    else:
        return f"In {days_until} days"

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main Streamlit application."""
    
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'service' not in st.session_state:
        st.session_state.service = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'events' not in st.session_state:
        st.session_state.events = []
    if 'last_scan' not in st.session_state:
        st.session_state.last_scan = None
    
    # Main header
    st.markdown('<h1 class="main-header">📧 Smart Email Reminder Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Automatically find deadlines and events hiding in your inbox</p>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown('<h2>⚙️ Settings</h2>', unsafe_allow_html=True)
        
        # Authentication section
        if not st.session_state.authenticated:
            st.markdown("### 🔐 Authentication")
            st.info("Connect your Gmail account to start scanning for reminders.")
            
            if st.button("🔑 Authenticate with Google", type="primary"):
                with st.spinner("Authenticating with Google..."):
                    service, user_email = get_gmail_service()
                    
                    if service and user_email:
                        st.session_state.service = service
                        st.session_state.user_email = user_email
                        st.session_state.authenticated = True
                        st.success(f"✅ Successfully authenticated!")
                        st.rerun()
                    else:
                        st.error("❌ Authentication failed. Please try again.")
        
        else:
            # Authenticated state
            st.success(f"✅ Authenticated as: {st.session_state.user_email}")
            
            # Scan controls
            st.markdown("### 📊 Scan Settings")
            
            scan_days = st.selectbox(
                "📅 Scan emails from last:",
                [1, 3, 7, 14, 30],
                index=2,
                format_func=lambda x: f"{x} day{'s' if x > 1 else ''}"
            )
            
            max_emails = st.slider(
                "📧 Maximum emails to scan:",
                min_value=10,
                max_value=100,
                value=50,
                step=10
            )
            
            # Scan button
            if st.button("🔍 Scan Inbox for Reminders", type="primary"):
                with st.spinner("🔍 Scanning your inbox... This may take a moment."):
                    # Progress bar
                    progress_bar = st.progress(0)
                    
                    # Search for emails
                    query = f"newer_than:{scan_days}d"
                    messages = search_emails(st.session_state.service, query, max_emails)
                    progress_bar.progress(25)
                    
                    if not messages:
                        st.info(f"📭 No emails found in the last {scan_days} days.")
                        st.session_state.events = []
                    else:
                        all_events = []
                        total_messages = len(messages)
                        
                        # Process each email
                        for i, message in enumerate(messages):
                            try:
                                raw_email = get_raw_email(st.session_state.service, message['id'])
                                if raw_email:
                                    parsed_email = parse_raw_email(raw_email)
                                    
                                    # Combine subject and body for analysis
                                    full_text = f"{parsed_email.get('subject', '')} {parsed_email.get('body', '')}"
                                    events = find_actionable_events(full_text)
                                    
                                    # Add source information to events
                                    for event in events:
                                        event['email_subject'] = parsed_email.get('subject', 'No Subject')
                                        event['email_from'] = parsed_email.get('from', 'Unknown Sender')
                                    
                                    all_events.extend(events)
                                
                                # Update progress
                                progress = 25 + (i + 1) / total_messages * 75
                                progress_bar.progress(int(progress))
                                
                            except Exception as e:
                                st.warning(f"⚠️ Error processing email: {e}")
                                continue
                        
                        # Remove duplicates and sort by urgency and date
                        unique_events = []
                        seen = set()
                        
                        for event in all_events:
                            event_key = (event['original_text'], event['parsed_date'].date())
                            if event_key not in seen:
                                seen.add(event_key)
                                unique_events.append(event)
                        
                        # Sort by urgency (high first) then by date
                        urgency_order = {"high": 0, "medium": 1, "low": 2}
                        unique_events.sort(key=lambda x: (urgency_order.get(x['urgency_color'], 3), x['parsed_date']))
                        
                        st.session_state.events = unique_events
                        st.session_state.last_scan = datetime.now()
                        
                    progress_bar.progress(100)
                    time.sleep(0.5)  # Brief pause to show completion
                    st.rerun()
            
            # Last scan info
            if st.session_state.last_scan:
                st.markdown("---")
                st.caption(f"🕒 Last scan: {st.session_state.last_scan.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Logout button
            st.markdown("---")
            if st.button("🚪 Logout"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    # Main content area
    if st.session_state.authenticated and st.session_state.events:
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
                <div class="stat-card">
                    <div class="stat-number">{len(st.session_state.events)}</div>
                    <div class="stat-label">Total Events</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            urgent_count = len([e for e in st.session_state.events if e['urgency_color'] == 'high'])
            st.markdown(f'''
                <div class="stat-card">
                    <div class="stat-number" style="color: var(--accent-color);">{urgent_count}</div>
                    <div class="stat-label">Urgent</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            upcoming_count = len([e for e in st.session_state.events if e['days_until'] >= 0])
            st.markdown(f'''
                <div class="stat-card">
                    <div class="stat-number" style="color: var(--success-color);">{upcoming_count}</div>
                    <div class="stat-label">Upcoming</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            overdue_count = len([e for e in st.session_state.events if e['days_until'] < 0])
            st.markdown(f'''
                <div class="stat-card">
                    <div class="stat-number" style="color: var(--warning-color);">{overdue_count}</div>
                    <div class="stat-label">Overdue</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Events display
        st.markdown("## 📅 Your Upcoming Events & Deadlines")
        
        if st.session_state.events:
            # Create responsive grid
            cols = st.columns(2)
            
            for i, event in enumerate(st.session_state.events):
                with cols[i % 2]:
                    urgency_emoji = get_urgency_emoji(event['urgency_color'])
                    time_until = format_time_until(event['days_until'])
                    
                    st.markdown(f'''
                        <div class="event-card event-urgency-{event['urgency_color']}">
                            <div class="event-title">
                                {urgency_emoji} {event['context'][:100]}{'...' if len(event['context']) > 100 else ''}
                            </div>
                            <div class="event-date">
                                🗓️ {event['formatted_date']} ({time_until})
                            </div>
                            <div class="event-source">
                                ✉️ From: {event['email_subject'][:50]}{'...' if len(event['email_subject']) > 50 else ''}
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
        
        else:
            st.info("📭 No upcoming events or deadlines found in your recent emails.")
    
    elif st.session_state.authenticated:
        # Authenticated but no scan yet
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h3>🎯 Ready to Scan Your Inbox!</h3>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Click "Scan Inbox for Reminders" in the sidebar to find important events and deadlines in your emails.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Not authenticated
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h3>🔐 Get Started</h3>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Authenticate with your Google account to begin scanning your emails for important reminders.
            </p>
            <p style="color: var(--text-secondary); margin-top: 2rem;">
                <strong>Features:</strong><br>
                🤖 AI-powered event detection<br>
                📅 Smart date parsing<br>
                🎯 Priority-based organization<br>
                🔒 Secure OAuth authentication
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()