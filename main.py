"""
Main Orchestration & Scheduling Script for Smart Email Reminder System

This script ties all modules together and runs them on a schedule to create
a fully autonomous email reminder system.

Required packages:
pip install schedule

For production deployment, consider using system schedulers like cron
for better reliability and resource management.
"""

import schedule
import time
from datetime import datetime
import sys
import os

# Import functions from our custom modules
try:
    from auth import get_gmail_service
    from email_fetcher import search_emails, get_raw_email
    from email_parser import parse_raw_email
    from intelligence_module import find_actionable_events
    from notifier import send_desktop_notification, format_event_notification, send_email_reminder
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Ensure all module files are in the same directory")
    sys.exit(1)


def run_reminder_workflow():
    """
    Execute the complete end-to-end email reminder workflow.
    
    This function orchestrates all modules to:
    1. Authenticate with Gmail
    2. Search for recent unread emails
    3. Parse email content
    4. Extract actionable events using NLP
    5. Send notifications for upcoming events
    """
    print("\n" + "="*60)
    print(f"🚀 Starting Email Reminder Workflow - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Step 1: Authentication
    print("🔐 Step 1: Authenticating with Gmail...")
    service = get_gmail_service()
    
    if not service:
        print("❌ Authentication failed. Cannot proceed with workflow.")
        return
    
    print("✅ Successfully authenticated with Gmail")
    
    # Step 2: Search for emails
    print("\n📧 Step 2: Searching for recent unread emails...")
    
    # Search for unread emails from the last day
    query = "is:unread newer_than:1d"
    messages = search_emails(service, query)
    
    if not messages:
        print("📭 No new unread emails found.")
        return
    
    print(f"📬 Found {len(messages)} unread email(s) to process")
    
    # Step 3: Process each email
    total_events_found = 0
    processed_emails = 0
    
    for i, message in enumerate(messages, 1):
        message_id = message['id']
        print(f"\n🔍 Step 3.{i}: Processing email ID: {message_id}")
        
        # Fetch raw email content
        raw_email_bytes = get_raw_email(service, message_id)
        
        if not raw_email_bytes:
            print(f"❌ Failed to fetch content for email {message_id}")
            continue
        
        # Parse email content
        parsed_email = parse_raw_email(raw_email_bytes)
        
        if not parsed_email or not parsed_email.get('body'):
            print(f"❌ Failed to parse email {message_id} or no body content")
            continue
        
        print(f"✅ Parsed email from: {parsed_email.get('from', 'Unknown')}")
        print(f"   Subject: {parsed_email.get('subject', 'No subject')[:50]}...")
        
        # Extract actionable events using NLP
        print("🧠 Analyzing email content for actionable events...")
        
        # Combine subject and body for comprehensive analysis
        full_text = f"{parsed_email.get('subject', '')} {parsed_email.get('body', '')}"
        actionable_events = find_actionable_events(full_text)
        
        if actionable_events:
            print(f"✅ Found {len(actionable_events)} actionable event(s)")
            total_events_found += len(actionable_events)
            
            # Step 4: Send notifications for each event
            for j, event in enumerate(actionable_events, 1):
                print(f"\n🔔 Step 4.{i}.{j}: Sending notification for event...")
                
                # Format notification content
                title, message = format_event_notification(
                    event, 
                    parsed_email.get('subject', '')
                )
                
                # Send desktop notification
                success = send_desktop_notification(title, message)

                if success:
                    print(f"✅ Notification sent for: {event.get('original_text', 'Unknown event')}")
                else:
                    print(f"❌ Failed to send notification for: {event.get('original_text', 'Unknown event')}")
                    # Fallback: Show console notification
                    print("\n" + "="*60)
                    print("🔔 CONSOLE NOTIFICATION (Desktop notification failed)")
                    print("="*60)
                    print(f"📅 {title}")
                    print(f"📝 {message}")
                    print("="*60)

                # Always send email reminder to self for backup
                recipient_email = os.getenv("SENDER_EMAIL")  # Send to the same email used for sending
                if recipient_email:
                    email_body = f"""🔔 Smart Email Reminder

📅 {title}

📝 {message}

📧 Original Email Subject: {parsed_email.get('subject', 'N/A')}
👤 From: {parsed_email.get('from', 'N/A')}
🕒 Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
This reminder was automatically generated by the Smart Email Reminder System.
"""
                    send_email_reminder(recipient_email, f"📅 {title}", email_body)
                else:
                    print("⚠️  No SENDER_EMAIL configured - skipping email reminder")
        else:
            print("📝 No actionable events found in this email")
        
        processed_emails += 1
    
    # Workflow summary
    print("\n" + "="*60)
    print("📊 WORKFLOW SUMMARY")
    print("="*60)
    print(f"📧 Emails processed: {processed_emails}")
    print(f"🎯 Total actionable events found: {total_events_found}")
    print(f"⏰ Workflow completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


def run_once_and_exit():
    """
    Run the workflow once and exit. Useful for cron jobs.
    """
    try:
        run_reminder_workflow()
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        sys.exit(1)
    
    print("✅ Single workflow execution completed. Exiting.")
    sys.exit(0)


if __name__ == '__main__':
    """
    Main entry point for the Smart Email Reminder System.
    
    Supports two modes:
    1. Continuous scheduling (default) - runs every 15 minutes
    2. Single execution (--once flag) - runs once and exits (for cron)
    """
    
    print("🎯 Smart Email Reminder System Starting...")
    print("=" * 60)
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        print("🔄 Running in single-execution mode (suitable for cron)")
        run_once_and_exit()
    
    # Development/continuous mode with schedule library
    print("🔄 Running in continuous scheduling mode")
    print("💡 For production, consider using system cron instead")
    print()
    
    # Schedule the workflow to run every 15 minutes
    schedule.every(15).minutes.do(run_reminder_workflow)
    
    # Also run once immediately
    print("🚀 Running initial workflow...")
    run_reminder_workflow()
    
    print(f"\n⏰ Scheduled to run every 15 minutes. Next run at: {schedule.next_run()}")
    print("🛑 Press Ctrl+C to stop the scheduler")
    
    try:
        # Main scheduling loop
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
        print("✅ Smart Email Reminder System shutdown complete")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error in scheduler: {e}")
        sys.exit(1)


"""
For production deployment, it's more robust to use a system scheduler like cron.
This provides better reliability, resource management, and error handling.

To use with cron, modify this script to run once and exit, rather than using 
the schedule loop. Use the --once flag for this purpose.

Example cron job (runs every 15 minutes):
*/15 * * * * cd /path/to/your/project && /usr/bin/python3 main.py --once >> cron.log 2>&1

Example cron job (runs every hour):
0 * * * * cd /path/to/your/project && /usr/bin/python3 main.py --once >> cron.log 2>&1

Example cron job (runs twice daily at 9 AM and 5 PM):
0 9,17 * * * cd /path/to/your/project && /usr/bin/python3 main.py --once >> cron.log 2>&1

For Windows Task Scheduler, create a task that runs:
Program: python
Arguments: main.py --once
Start in: D:\\Path\\To\\Your\\Project\\
"""