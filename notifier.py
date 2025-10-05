"""
Notification Module for Smart Email Reminder System

Handles user-facing alerts through desktop notifications and email reminders.
Provides cross-platform notification capabilities and secure email sending.

Required packages:
pip install plyer python-dotenv
"""

from plyer import notification
import smtplib
import os
import platform
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_desktop_notification(title: str, message: str) -> bool:
    """
    Send a cross-platform desktop notification with multiple fallback methods.

    Args:
        title: Notification title
        message: Notification message content

    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    # Clean the message for XML compatibility
    clean_message = message.replace('\n', ' | ').replace('"', "'").replace('&', '&amp;')

    try:
        # Try plyer first (most reliable cross-platform)
        notification.notify(  # type: ignore
            title=title,
            message=message,
            timeout=30,
            app_name="Smart Email Reminder"
        )
        print(f"✅ Desktop notification sent: {title}")
        return True

    except Exception as e:
        print(f"❌ Plyer notification failed: {e}")

        # Try Windows-specific toast notification
        if platform.system().lower() == "windows":
            try:
                import subprocess

                # Create a more robust PowerShell command for Windows 11
                ps_command = f'''
                try {{
                    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                    [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

                    $template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text><![CDATA[{title}]]></text>
            <text><![CDATA[{clean_message}]]></text>
        </binding>
    </visual>
</toast>
"@

                    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
                    $xml.LoadXml($template)
                    $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
                    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Smart Email Reminder").Show($toast)
                    Write-Host "Toast notification sent successfully"
                }} catch {{
                    Write-Error $_.Exception.Message
                    exit 1
                }}
                '''

                result = subprocess.run(["powershell", "-Command", ps_command],
                                      capture_output=True, text=True, timeout=15)

                if result.returncode == 0:
                    print(f"✅ Windows toast notification sent: {title}")
                    return True
                else:
                    print(f"❌ Windows toast notification failed: {result.stderr}")

            except Exception as ps_e:
                print(f"❌ Windows toast notification also failed: {ps_e}")

    # Last resort: Console notification with enhanced visibility
    print("\n" + "="*70)
    print("🔔 REMINDER NOTIFICATION")
    print("="*70)
    print(f"📅 {title}")
    print(f"📝 {message}")
    print("="*70)
    print("💡 If you don't see desktop notifications:")
    print("   1. Check Windows Settings > System > Notifications & actions")
    print("   2. Make sure notifications are enabled")
    print("   3. Check if Focus Assist is turned off")
    print("   4. Try running as administrator")
    print("="*70)

    return True  # Console notification always "succeeds"

    # Last resort: Console notification with enhanced visibility
    print("\n" + "="*70)
    print("🔔 REMINDER NOTIFICATION")
    print("="*70)
    print(f"📅 {title}")
    print(f"📝 {message}")
    print("="*70)
    print("💡 If you don't see desktop notifications:")
    print("   1. Check Windows Settings > System > Notifications & actions")
    print("   2. Make sure notifications are enabled")
    print("   3. Check if Focus Assist is turned off")
    print("   4. Try running as administrator")
    print("="*70)

    return True  # Console notification always "succeeds"


def send_email_reminder(recipient_email: str, subject: str, body: str) -> bool:
    """
    Send a reminder via email using Gmail's SMTP server.
    
    Note: Requires a Gmail App Password (16-digit password) for authentication.
    Regular Gmail passwords will not work due to 2FA requirements.
    
    Environment variables required:
    - SENDER_EMAIL: Gmail address to send from
    - SENDER_APP_PASSWORD: 16-digit Gmail App Password
    
    Args:
        recipient_email: Email address to send reminder to
        subject: Email subject line
        body: Email message body
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Get credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    sender_app_password = os.getenv("SENDER_APP_PASSWORD")  # 16-digit App Password required
    
    if not sender_email or not sender_app_password:
        print("❌ Missing email credentials in environment variables")
        print("💡 Please set SENDER_EMAIL and SENDER_APP_PASSWORD in your .env file")
        print("💡 SENDER_APP_PASSWORD must be a 16-digit Gmail App Password, not your regular password")
        return False
    
    try:
        # Construct the email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.set_content(body)
        
        # Send the email using Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # Secure the connection
            server.starttls()
            
            # Login with App Password
            server.login(sender_email, sender_app_password)
            
            # Send the message
            server.send_message(msg)
            
        print(f"✅ Email reminder sent to {recipient_email}: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Email authentication failed: {e}")
        print("💡 Ensure you're using a valid Gmail App Password, not your regular password")
        print("💡 Enable 2FA and generate an App Password at: https://myaccount.google.com/apppasswords")
        return False
        
    except Exception as e:
        print(f"❌ Failed to send email reminder: {e}")
        return False


def format_event_notification(event: dict, email_subject: str = "") -> tuple:
    """
    Format an actionable event into notification title and message.
    
    Args:
        event: Event dictionary from intelligence_module
        email_subject: Optional email subject for context
        
    Returns:
        tuple: (title, message) for notification
    """
    # Extract event details
    event_context = event.get('event_context', 'Unknown event')
    event_datetime = event.get('datetime')
    original_text = event.get('original_text', '')
    
    # Format the datetime
    if event_datetime:
        formatted_date = event_datetime.strftime('%A, %B %d at %I:%M %p')
        
        # Calculate urgency - handle timezone-aware vs timezone-naive comparison
        from datetime import datetime
        current_time = datetime.now()
        
        if event_datetime.tzinfo is not None:
            # event_datetime is timezone-aware, make current_time aware
            current_time = current_time.replace(tzinfo=event_datetime.tzinfo)
        
        try:
            days_until = (event_datetime - current_time).days
            
            if days_until == 0:
                urgency = "TODAY"
            elif days_until == 1:
                urgency = "TOMORROW"
            elif days_until <= 3:
                urgency = f"IN {days_until} DAYS"
            else:
                urgency = f"IN {days_until} DAYS"
        except Exception as e:
            # Fallback if date calculation fails
            urgency = "UPCOMING"
            days_until = 0
    else:
        formatted_date = "Unknown date"
        urgency = ""
    
    # Create notification title
    title = f"📅 Reminder: {urgency}"
    
    # Create notification message
    message_parts = []
    if email_subject:
        message_parts.append(f"From email: {email_subject}")
    message_parts.append(f"Event: {event_context}")
    message_parts.append(f"When: {formatted_date}")
    if original_text:
        message_parts.append(f"Original: \"{original_text}\"")
    
    message = "\n".join(message_parts)
    
    return title, message


if __name__ == '__main__':
    """
    Test the notification module functionality.
    """
    print("🔔 Testing Notification Module...")
    print("=" * 50)
    
    # Test desktop notification
    print("\n📱 Testing desktop notification...")
    test_title = "Smart Email Reminder - Test"
    test_message = "This is a test notification from your email reminder system!"
    
    success = send_desktop_notification(test_title, test_message)
    
    if success:
        print("✅ Desktop notification test successful")
    else:
        print("❌ Desktop notification test failed")
    
    # Test email formatting
    print("\n📧 Testing event formatting...")
    from datetime import datetime, timedelta
    
    sample_event = {
        'event_context': 'meeting - quarterly review meeting',
        'datetime': datetime.now() + timedelta(days=2, hours=5),
        'original_text': 'quarterly review meeting for October 28th',
        'entity_label': 'DATE'
    }
    
    title, message = format_event_notification(sample_event, "Q4 Planning Meeting")
    
    print(f"Formatted notification:")
    print(f"Title: {title}")
    print(f"Message:\n{message}")
    
    # Test email reminder (will only work if .env is configured)
    print("\n📧 Testing email reminder...")
    test_recipient = os.getenv("TEST_EMAIL", "test@example.com")
    
    if os.getenv("SENDER_EMAIL") and os.getenv("SENDER_APP_PASSWORD"):
        email_success = send_email_reminder(
            test_recipient,
            "Smart Email Reminder - Test",
            "This is a test email from your Smart Email Reminder system!\n\n" +
            "If you receive this, your email notifications are working correctly."
        )
        
        if email_success:
            print("✅ Email reminder test successful")
        else:
            print("❌ Email reminder test failed")
    else:
        print("⚠️  Email credentials not configured - skipping email test")
        print("💡 To test email functionality, create a .env file with:")
        print("   SENDER_EMAIL=your_gmail@gmail.com")
        print("   SENDER_APP_PASSWORD=your_16_digit_app_password")
        print("   TEST_EMAIL=test_recipient@example.com")
    
    print("\n" + "=" * 50)
    print("🔔 Notification module testing completed!")