"""
Content Parsing & Extraction Module for Smart Email Reminder System

This module transforms raw email bytes into structured, clean format for analysis.
Handles complex email formats, multipart messages, and various character encodings.
"""

import email
from email.message import Message
from email.header import decode_header, make_header


def decode_email_header(header_string):
    """
    Handle potentially encoded email headers (as specified in RFC 2047).
    
    Args:
        header_string: Raw header string that may contain encoded content
        
    Returns:
        str: Decoded, human-readable header string
    """
    if not header_string:
        return ""
    
    try:
        # Get a list of decoded parts using decode_header()
        decoded_parts = decode_header(header_string)
        
        # Use make_header() to correctly join these parts into a single string
        decoded_header = make_header(decoded_parts)
        
        # Convert to string and return
        return str(decoded_header)
    
    except Exception as e:
        print(f"Warning: Could not decode header '{header_string}': {e}")
        return str(header_string)


def get_email_body(email_message):
    """
    Extract clean plain text from email body, handling multipart messages.
    
    Args:
        email_message: email.message.Message object
        
    Returns:
        str: Clean, decoded email body text
    """
    if not isinstance(email_message, Message):
        print("Error: Invalid email message object")
        return ""
    
    # Check if the message is multipart
    if email_message.is_multipart():
        # Iterate through all parts of the email using walk()
        for part in email_message.walk():
            # Check if this part is plain text and not an attachment
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))
            
            if (content_type == 'text/plain' and 
                'attachment' not in content_disposition):
                
                # Get character set with utf-8 as fallback
                charset = part.get_content_charset() or 'utf-8'
                
                try:
                    # Decode the payload
                    payload = part.get_payload(decode=True)
                    if payload:
                        # Handle different payload types
                        if isinstance(payload, bytes):
                            # Decode using the determined character set with error handling
                            body = payload.decode(charset, errors='replace')
                            return body.strip()
                        elif isinstance(payload, str):
                            # Already decoded, return as is
                            return payload.strip()
                except Exception as e:
                    print(f"Warning: Could not decode email part: {e}")
                    continue
    
    else:
        # Handle non-multipart messages
        try:
            # Get character set with utf-8 as fallback
            charset = email_message.get_content_charset() or 'utf-8'
            
            # Get the main payload directly
            payload = email_message.get_payload(decode=True)
            if payload:
                # Handle different payload types
                if isinstance(payload, bytes):
                    # Decode using the same charset logic
                    body = payload.decode(charset, errors='replace')
                    return body.strip()
                elif isinstance(payload, str):
                    # Already decoded, return as is
                    return payload.strip()
        except Exception as e:
            print(f"Warning: Could not decode email body: {e}")
    
    return ""


def parse_raw_email(raw_email_bytes):
    """
    Primary entry point for parsing raw email bytes into structured data.
    
    Args:
        raw_email_bytes: Raw email content as bytes
        
    Returns:
        dict: Parsed email data with keys: subject, from, to, body
    """
    if not raw_email_bytes:
        print("Error: No raw email bytes provided")
        return {'subject': '', 'from': '', 'to': '', 'body': ''}
    
    try:
        # Create the email.message.Message object from raw bytes
        email_message = email.message_from_bytes(raw_email_bytes)
        
        # Extract headers
        raw_subject = email_message.get('Subject', '')
        raw_from = email_message.get('From', '')
        raw_to = email_message.get('To', '')
        
        # Decode headers using our helper function
        subject = decode_email_header(raw_subject)
        from_address = decode_email_header(raw_from)
        to_address = decode_email_header(raw_to)
        
        # Get clean body text
        body = get_email_body(email_message)
        
        # Return structured data
        return {
            'subject': subject,
            'from': from_address,
            'to': to_address,
            'body': body
        }
    
    except Exception as e:
        print(f"Error parsing email: {e}")
        return {'subject': '', 'from': '', 'to': '', 'body': ''}


if __name__ == '__main__':
    """
    Test the email parsing functionality by fetching and parsing a recent email.
    """
    print("🔍 Testing Email Parsing & Extraction Module...")
    
    try:
        # Import functions from previous modules
        from auth import get_gmail_service
        from email_fetcher import search_emails, get_raw_email
        
        # Get authenticated service
        print("📧 Authenticating with Gmail...")
        service = get_gmail_service()
        
        if not service:
            print("❌ Failed to authenticate with Gmail service")
            exit(1)
        
        # Search for recent emails (last 7 days, limit to 1)
        print("🔎 Searching for recent emails...")
        query = "newer_than:7d"
        messages = search_emails(service, query)
        
        if not messages:
            print("❌ No recent emails found to test with")
            exit(1)
        
        # Get the first message
        message_id = messages[0]['id']
        print(f"📩 Fetching email with ID: {message_id}")
        
        # Fetch raw email content
        raw_email_bytes = get_raw_email(service, message_id)
        
        if not raw_email_bytes:
            print("❌ Failed to fetch raw email content")
            exit(1)
        
        # Parse the email
        print("🔧 Parsing email content...")
        parsed_email = parse_raw_email(raw_email_bytes)
        
        # Display results in a clean format
        print("\n" + "="*60)
        print("📧 PARSED EMAIL CONTENT")
        print("="*60)
        print(f"Subject: {parsed_email['subject']}")
        print(f"From: {parsed_email['from']}")
        print(f"To: {parsed_email['to']}")
        print("\nBody Preview (first 500 characters):")
        print("-" * 40)
        body_preview = parsed_email['body'][:500]
        if len(parsed_email['body']) > 500:
            body_preview += "..."
        print(body_preview)
        print("-" * 40)
        print(f"Total body length: {len(parsed_email['body'])} characters")
        print("="*60)
        print("✅ Email parsing completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure auth.py and email_fetcher.py are in the same directory")
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")