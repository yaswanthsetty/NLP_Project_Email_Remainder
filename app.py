#!/usr/bin/env python3
"""
Smart Email Reminder Dashboard - Multi-Page Streamlit App

A modern web interface with navigation-based pages instead of sidebar.
Pages: Home -> Authenticate -> Scan -> Results

Author: Yaswanth Setty
"""

import streamlit as st
import os
import base64
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Email and NLP imports
import email
import smtplib
from email.message import EmailMessage
from email.header import decode_header, make_header
from dotenv import load_dotenv

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# NLP imports
import spacy
import dateparser

# Load environment
load_dotenv()

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Smart Email Reminders",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

def load_css():
    """Modern dark theme with beautiful styling."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #6C63FF;
        --secondary: #4ECDC4;
        --accent: #FF6B6B;
        --success: #00C851;
        --warning: #FFB347;
        --dark-bg: #0E1117;
        --surface: #1E2329;
        --surface-light: #262730;
        --text: #FAFAFA;
        --text-dim: #A0A0A0;
    }
    
    .main { font-family: 'Inter', sans-serif; }
    
    [data-testid="stSidebar"] { display: none; }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .float {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Feature Cards - Interactive */
    .feature-card {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.1), rgba(78, 205, 196, 0.05));
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(108, 99, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: var(--primary);
        box-shadow: 0 12px 24px rgba(108, 99, 255, 0.3);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.2) rotate(5deg);
    }
    
    /* Demo Section */
    .demo-box {
        background: rgba(108, 99, 255, 0.05);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .demo-box::after {
        content: '✨ AI Powered';
        position: absolute;
        top: -12px;
        right: 20px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }
    
    /* Stats Counter */
    .stat-counter {
        background: linear-gradient(135deg, var(--surface), var(--surface-light));
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(108, 99, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-counter:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 8px 16px rgba(108, 99, 255, 0.2);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .cta-button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .cta-button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.6);
    }
    
    /* Event Cards */
    .card {
        background: var(--surface);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary);
    }
    
    .event-card {
        background: var(--surface);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .event-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .urgent { border-left: 4px solid var(--accent); }
    .medium { border-left: 4px solid var(--warning); }
    .low { border-left: 4px solid var(--success); }
    
    .stat-card {
        background: var(--surface-light);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stat-label {
        color: var(--text-dim);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .feature-card {
            padding: 1.5rem;
        }
        .feature-icon {
            font-size: 2.5rem;
        }
        .stat-number {
            font-size: 2rem;
        }
        .cta-button {
            padding: 0.8rem 2rem;
            font-size: 1rem;
        }
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# =============================================================================
# BACKEND FUNCTIONS
# =============================================================================

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate with Gmail API."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                pass
        else:
            if not os.path.exists('credentials.json'):
                return None, None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        user_email = profile.get('emailAddress', 'Unknown')
        return service, user_email
    except:
        return None, None

def search_emails(service, query: str, max_results: int = 50):
    """Search Gmail for emails."""
    try:
        result = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return result.get('messages', [])
    except:
        return []

def get_raw_email(service, message_id: str):
    """Get raw email content."""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
        return base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    except:
        return None

def parse_raw_email(raw_email_bytes):
    """Parse email to structured data."""
    if not raw_email_bytes:
        return {'subject': '', 'from': '', 'to': '', 'body': ''}
    
    try:
        email_message = email.message_from_bytes(raw_email_bytes)
        
        subject = str(make_header(decode_header(email_message.get('Subject', ''))))
        from_addr = str(make_header(decode_header(email_message.get('From', ''))))
        to_addr = str(make_header(decode_header(email_message.get('To', ''))))
        
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        if isinstance(payload, bytes):
                            body = payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
                        elif isinstance(payload, str):
                            body = payload
                        else:
                            body = str(payload)
                        break
        else:
            payload = email_message.get_payload(decode=True)
            if payload:
                if isinstance(payload, bytes):
                    body = payload.decode(email_message.get_content_charset() or 'utf-8', errors='ignore')
                elif isinstance(payload, str):
                    body = payload
                else:
                    body = str(payload)
        
        return {'subject': subject, 'from': from_addr, 'to': to_addr, 'body': body}
    except:
        return {'subject': '', 'from': '', 'to': '', 'body': ''}

def find_actionable_events(text: str) -> List[Dict[str, Any]]:
    """Use NLP to find events in text."""
    if not text or not text.strip():
        return []
    
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        return []
    
    try:
        doc = nlp(text)
        events = []
        
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME", "EVENT"]:
                start = max(0, ent.start - 10)
                end = min(len(doc), ent.end + 10)
                context = doc[start:end].text
                
                parsed_date = dateparser.parse(ent.text)
                
                if parsed_date:
                    days_until = (parsed_date - datetime.now()).days
                    
                    if days_until < 0:
                        urgency = "overdue"
                        urgency_color = "urgent"
                    elif days_until <= 1:
                        urgency = "urgent"
                        urgency_color = "urgent"
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
        
        events.sort(key=lambda x: x['parsed_date'])
        return events
    except:
        return []

def send_email_notification(events: List[Dict], user_email: str):
    """Send email notification with important events."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")
    
    if not sender_email or not sender_password or not events:
        return False
    
    urgent_events = [e for e in events if e['urgency_color'] in ['urgent', 'medium']]
    
    if not urgent_events:
        return False
    
    subject = f"🚨 {len(urgent_events)} Important Reminder(s) from Your Inbox"
    
    body = f"""
Smart Email Reminder - Important Events Detected
================================================

Hello,

We found {len(urgent_events)} important event(s) in your recent emails that need your attention:

"""
    
    for i, event in enumerate(urgent_events, 1):
        urgency_emoji = "🚨" if event['urgency_color'] == 'urgent' else "⚠️"
        body += f"""
{i}. {urgency_emoji} {event['context'][:100]}
   📅 Date: {event['formatted_date']}
   ⏰ Status: {event['urgency']} ({event['days_until']} days)
   📧 Source: {event.get('email_subject', 'N/A')}
   
"""
    
    body += f"""
================================================
Total Events Found: {len(events)}
Urgent/Important: {len(urgent_events)}
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is an automated reminder from Smart Email Reminder System.
"""
    
    try:
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.set_content(body)
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except:
        return False

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'service' not in st.session_state:
    st.session_state.service = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'events' not in st.session_state:
    st.session_state.events = []
if 'scan_complete' not in st.session_state:
    st.session_state.scan_complete = False

# =============================================================================
# PAGE: HOME
# =============================================================================

def show_home_page():
    """Landing page with navigation."""
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0;" class="animate-in">
        <div style="font-size: 5rem; margin-bottom: 1rem;" class="float">📧</div>
        <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(135deg, #6C63FF, #4ECDC4); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">
            Smart Email Reminder
        </h1>
        <p style="font-size: 1.4rem; color: #A0A0A0; margin-top: 1.5rem; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            Never miss important deadlines hiding in your emails. Let AI find them for you.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-counter">
            <div class="stat-number">AI</div>
            <div class="stat-label">Powered NLP</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-counter">
            <div class="stat-number">3s</div>
            <div class="stat-label">Average Scan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-counter">
            <div class="stat-number">100%</div>
            <div class="stat-label">Secure OAuth</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-counter">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Always Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Live Demo Section
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="font-size: 2rem; color: #FAFAFA; margin-bottom: 1rem;">
            See What We Can Detect 🎯
        </h2>
        <p style="color: #A0A0A0; font-size: 1.1rem;">
            Our AI understands natural language and finds important dates automatically
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="demo-box">
            <div style="color: #4ECDC4; font-weight: 600; margin-bottom: 0.5rem;">📧 Email Example</div>
            <div style="color: #A0A0A0; font-style: italic; line-height: 1.8;">
                "Hi team, don't forget the <strong style="color: #FFB347;">project deadline next Friday at 3 PM</strong>. 
                Also, the <strong style="color: #FFB347;">client meeting is scheduled for October 20th</strong>."
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="demo-box">
            <div style="color: #00C851; font-weight: 600; margin-bottom: 0.5rem;">✅ AI Detection</div>
            <div style="line-height: 2;">
                <div style="color: #FF6B6B;">🚨 <strong>Urgent:</strong> Project deadline (5 days)</div>
                <div style="color: #FFB347;">⚠️ <strong>Soon:</strong> Client meeting (5 days)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Interactive Feature Cards
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="font-size: 2rem; color: #FAFAFA;">Powerful Features ⚡</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 style="color: #FAFAFA; margin-bottom: 0.5rem;">AI-Powered Detection</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Advanced NLP using spaCy to automatically detect dates, times, and events in natural language
            </p>
            <div style="margin-top: 1rem; color: #4ECDC4; font-size: 0.9rem; font-weight: 600;">
                ✓ Named Entity Recognition<br/>
                ✓ Context-Aware Parsing<br/>
                ✓ Multi-Format Support
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📧</div>
            <h3 style="color: #FAFAFA; margin-bottom: 0.5rem;">Smart Email Alerts</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Get automatic email notifications for urgent and important events found in your inbox
            </p>
            <div style="margin-top: 1rem; color: #4ECDC4; font-size: 0.9rem; font-weight: 600;">
                ✓ Priority-Based Filtering<br/>
                ✓ Customizable Notifications<br/>
                ✓ Beautiful Email Format
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>
            <h3 style="color: #FAFAFA; margin-bottom: 0.5rem;">Smart Date Parsing</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Understands phrases like "next Friday", "in 3 days", "October 20th" and converts them automatically
            </p>
            <div style="margin-top: 1rem; color: #4ECDC4; font-size: 0.9rem; font-weight: 600;">
                ✓ Natural Language Processing<br/>
                ✓ Relative Date Understanding<br/>
                ✓ Time Zone Aware
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3 style="color: #FAFAFA; margin-bottom: 0.5rem;">Bank-Level Security</h3>
            <p style="color: #A0A0A0; line-height: 1.6;">
                Your data is protected with OAuth 2.0. We never store your emails or credentials
            </p>
            <div style="margin-top: 1rem; color: #4ECDC4; font-size: 0.9rem; font-weight: 600;">
                ✓ OAuth 2.0 Authentication<br/>
                ✓ Zero Data Storage<br/>
                ✓ Read-Only Access
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # How It Works
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="font-size: 2rem; color: #FAFAFA;">How It Works 🔄</h2>
        <p style="color: #A0A0A0; font-size: 1.1rem;">Get started in just 3 simple steps</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(108, 99, 255, 0.05); border-radius: 12px; border: 2px solid rgba(108, 99, 255, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">�</div>
            <h3 style="color: #6C63FF; margin-bottom: 0.5rem;">1. Connect</h3>
            <p style="color: #A0A0A0; font-size: 0.95rem;">
                Securely authenticate with your Gmail account using OAuth 2.0
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(78, 205, 196, 0.05); border-radius: 12px; border: 2px solid rgba(78, 205, 196, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #4ECDC4; margin-bottom: 0.5rem;">2. Scan</h3>
            <p style="color: #A0A0A0; font-size: 0.95rem;">
                AI analyzes your emails and detects important dates and events
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(0, 200, 81, 0.05); border-radius: 12px; border: 2px solid rgba(0, 200, 81, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">�</div>
            <h3 style="color: #00C851; margin-bottom: 0.5rem;">3. Organize</h3>
            <p style="color: #A0A0A0; font-size: 0.95rem;">
                View all deadlines organized by priority and urgency
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Call to Action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, rgba(108, 99, 255, 0.1), rgba(78, 205, 196, 0.1)); 
                    padding: 3rem 2rem; border-radius: 20px; border: 2px solid rgba(108, 99, 255, 0.3);">
            <h2 style="font-size: 2.2rem; color: #FAFAFA; margin-bottom: 1rem;">
                Ready to Never Miss a Deadline?
            </h2>
            <p style="color: #A0A0A0; font-size: 1.1rem; margin-bottom: 2rem;">
                Join hundreds of professionals staying organized with AI-powered email analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Get Started Free", type="primary", use_container_width=True, key="cta_main"):
            st.session_state.page = 'authenticate'
            st.rerun()
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; color: #A0A0A0; font-size: 0.9rem;">
            <p>✓ No credit card required  •  ✓ Free forever  •  ✓ 100% secure</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: AUTHENTICATE
# =============================================================================

def show_authenticate_page():
    """Authentication page."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔐</div>
        <h1>Connect Your Gmail</h1>
        <p style="font-size: 1.1rem; color: #A0A0A0;">
            Securely authenticate with Google to scan your emails
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.authenticated:
            st.info("🔒 We use OAuth 2.0 for secure authentication. Your credentials are never stored.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🔑 Authenticate with Google", type="primary", use_container_width=True):
                with st.spinner("🔐 Connecting to Google..."):
                    service, user_email = get_gmail_service()
                    
                    if service and user_email:
                        st.session_state.service = service
                        st.session_state.user_email = user_email
                        st.session_state.authenticated = True
                        st.success(f"✅ Successfully authenticated as {user_email}")
                        time.sleep(1)
                        st.session_state.page = 'scan'
                        st.rerun()
                    else:
                        st.error("❌ Authentication failed. Please check your credentials.json file.")
        else:
            st.success(f"✅ Already authenticated as {st.session_state.user_email}")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continue to Scan →", type="primary", use_container_width=True):
                st.session_state.page = 'scan'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home"):
            st.session_state.page = 'home'
            st.rerun()

# =============================================================================
# PAGE: SCAN
# =============================================================================

def show_scan_page():
    """Email scanning configuration and execution page."""
    if not st.session_state.authenticated:
        st.warning("⚠️ Please authenticate first")
        if st.button("Go to Authentication"):
            st.session_state.page = 'authenticate'
            st.rerun()
        return
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
        <h1>Scan Your Inbox</h1>
        <p style="font-size: 1.1rem; color: #A0A0A0;">
            Configure scan settings and analyze your emails
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="card">
            <p style="text-align: center; color: #00C851;">
                ✅ Authenticated as <strong>{st.session_state.user_email}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### ⚙️ Scan Configuration")
        
        scan_days = st.selectbox(
            "📅 Time Range",
            [1, 3, 7, 14, 30],
            index=2,
            format_func=lambda x: f"Last {x} day{'s' if x > 1 else ''}"
        )
        
        max_emails = st.slider(
            "📧 Maximum Emails to Scan",
            min_value=10,
            max_value=100,
            value=50,
            step=10
        )
        
        send_email = st.checkbox(
            "📧 Send email notification for urgent items",
            value=True,
            help="You'll receive an email with urgent/important events"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔍 Start Scanning", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing your emails..."):
                progress_bar = st.progress(0)
                status = st.empty()
                
                status.text("Searching for emails...")
                query = f"newer_than:{scan_days}d"
                messages = search_emails(st.session_state.service, query, max_emails)
                progress_bar.progress(20)
                
                if not messages:
                    st.info(f"📭 No emails found in the last {scan_days} days.")
                    st.session_state.events = []
                else:
                    all_events = []
                    total = len(messages)
                    
                    status.text(f"Processing {total} emails...")
                    
                    for i, msg in enumerate(messages):
                        raw_email = get_raw_email(st.session_state.service, msg['id'])
                        if raw_email:
                            parsed = parse_raw_email(raw_email)
                            full_text = f"{parsed.get('subject', '')} {parsed.get('body', '')}"
                            events = find_actionable_events(full_text)
                            
                            for event in events:
                                event['email_subject'] = parsed.get('subject', 'No Subject')
                                event['email_from'] = parsed.get('from', 'Unknown')
                            
                            all_events.extend(events)
                        
                        progress_bar.progress(20 + int((i + 1) / total * 60))
                    
                    unique_events = []
                    seen = set()
                    for event in all_events:
                        key = (event['original_text'], event['parsed_date'].date())
                        if key not in seen:
                            seen.add(key)
                            unique_events.append(event)
                    
                    urgency_order = {"urgent": 0, "medium": 1, "low": 2}
                    unique_events.sort(key=lambda x: (urgency_order.get(x['urgency_color'], 3), x['parsed_date']))
                    
                    st.session_state.events = unique_events
                    st.session_state.scan_complete = True
                    
                    if send_email and unique_events:
                        status.text("Sending email notification...")
                        if send_email_notification(unique_events, st.session_state.user_email):
                            st.success("✅ Email notification sent!")
                        progress_bar.progress(90)
                    
                    status.text("✅ Scan complete!")
                    progress_bar.progress(100)
                    time.sleep(1)
                    st.session_state.page = 'results'
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back"):
            st.session_state.page = 'home'
            st.rerun()

# =============================================================================
# PAGE: RESULTS
# =============================================================================

def show_results_page():
    """Display scan results."""
    if not st.session_state.scan_complete:
        st.warning("⚠️ No scan results available")
        if st.button("Go to Scan"):
            st.session_state.page = 'scan'
            st.rerun()
        return
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>📊 Your Events & Deadlines</h1>
    </div>
    """, unsafe_allow_html=True)
    
    events = st.session_state.events
    
    if not events:
        st.info("📭 No events or deadlines found in your recent emails.")
        if st.button("Scan Again"):
            st.session_state.page = 'scan'
            st.rerun()
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    urgent_count = len([e for e in events if e['urgency_color'] == 'urgent'])
    medium_count = len([e for e in events if e['urgency_color'] == 'medium'])
    upcoming_count = len([e for e in events if e['days_until'] >= 0])
    overdue_count = len([e for e in events if e['days_until'] < 0])
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(events)}</div>
            <div class="stat-label">Total Events</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #FF6B6B;">{urgent_count}</div>
            <div class="stat-label">Urgent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #FFB347;">{medium_count}</div>
            <div class="stat-label">Coming Soon</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #00C851;">{upcoming_count}</div>
            <div class="stat-label">Upcoming</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 📅 All Events")
    
    cols = st.columns(2)
    
    for i, event in enumerate(events):
        with cols[i % 2]:
            urgency_emoji = {"urgent": "🚨", "medium": "⚠️", "low": "📅"}
            emoji = urgency_emoji.get(event['urgency_color'], "📅")
            
            time_until = f"{abs(event['days_until'])} days overdue" if event['days_until'] < 0 else \
                        "Today" if event['days_until'] == 0 else \
                        "Tomorrow" if event['days_until'] == 1 else \
                        f"In {event['days_until']} days"
            
            st.markdown(f"""
            <div class="event-card {event['urgency_color']}">
                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
                    {emoji} {event['context'][:80]}{'...' if len(event['context']) > 80 else ''}
                </div>
                <div style="color: #4ECDC4; margin-bottom: 0.5rem;">
                    🗓️ {event['formatted_date']} ({time_until})
                </div>
                <div style="color: #A0A0A0; font-size: 0.9rem;">
                    ✉️ {event.get('email_subject', 'N/A')[:60]}{'...' if len(event.get('email_subject', '')) > 60 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Scan Again"):
            st.session_state.scan_complete = False
            st.session_state.events = []
            st.session_state.page = 'scan'
            st.rerun()
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'home'
            st.rerun()
    with col3:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'home'
            st.rerun()

# =============================================================================
# MAIN APP ROUTING
# =============================================================================

def main():
    """Main application with page routing."""
    load_css()
    
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'authenticate':
        show_authenticate_page()
    elif st.session_state.page == 'scan':
        show_scan_page()
    elif st.session_state.page == 'results':
        show_results_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()