import base64
from googleapiclient.errors import HttpError
from auth import get_gmail_service

def search_emails(service, query):
    """
    Search for emails using Gmail API server-side filtering.
    
    Args:
        service: Authenticated Gmail API service object
        query: Gmail search query string (e.g., "is:unread newer_than:7d")
    
    Returns:
        List of message objects containing 'id' and 'threadId', or empty list if no messages found
    """
    if not service:
        print("Error: Gmail service object is None")
        return []
        
    try:
        # Perform server-side search using Gmail API
        result = service.users().messages().list(userId='me', q=query).execute()
        
        # Handle case where no messages are found
        messages = result.get('messages', [])
        
        if not messages:
            print(f"No messages found for query: {query}")
            return []
        
        print(f"Found {len(messages)} messages matching query: {query}")
        return messages
    
    except HttpError as error:
        print(f'An error occurred during email search: {error}')
        return []

def get_raw_email(service, message_id):
    """
    Fetch the complete raw content of a specific email message.
    
    Args:
        service: Authenticated Gmail API service object
        message_id: The Gmail message ID to fetch
    
    Returns:
        Raw email bytes (decoded from base64url), or None if error occurred
    """
    if not service:
        print("Error: Gmail service object is None")
        return None
        
    try:
        # Fetch the complete raw email content
        message = service.users().messages().get(
            userId='me', 
            id=message_id, 
            format='raw'
        ).execute()
        
        # Extract the base64url encoded raw data
        raw_data = message.get('raw')
        if not raw_data:
            print(f"No raw data found for message ID: {message_id}")
            return None
        
        # Decode the base64url encoded string into bytes
        raw_email_bytes = base64.urlsafe_b64decode(raw_data)
        
        return raw_email_bytes
    
    except HttpError as error:
        print(f'An error occurred fetching message {message_id}: {error}')
        return None

if __name__ == '__main__':
    # Test the email fetching functionality
    print("Testing Email Ingestion & Filtering Module...")
    
    # Check if credentials.json exists before attempting authentication
    import os
    if not os.path.exists('credentials.json'):
        print("❌ Missing credentials.json file!")
        print("\nTo test this module with real Gmail data:")
        print("1. Create a Google Cloud Project")
        print("2. Enable the Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download credentials.json to this directory")
        print("\nFor now, the module structure is validated ✅")
        print("Functions available:")
        print("  - search_emails(service, query)")
        print("  - get_raw_email(service, message_id)")
        exit(0)
    
    # Get authenticated Gmail service
    service = get_gmail_service()
    if not service:
        print("Failed to authenticate. Please check your credentials.")
        exit(1)
    
    # Define sample query - search for unread emails from the last 7 days
    query = "is:unread newer_than:7d"
    print(f"Searching for emails with query: {query}")
    
    # Search for emails
    messages = search_emails(service, query)
    
    if messages:
        print(f"\nProcessing first {min(5, len(messages))} messages:")
        
        # Process first 5 messages (or fewer if not enough found)
        for i, message in enumerate(messages[:5], 1):
            message_id = message['id']
            print(f"\n{i}. Processing message ID: {message_id}")
            
            # Fetch raw email content
            raw_email_bytes = get_raw_email(service, message_id)
            
            if raw_email_bytes:
                print(f"   ✓ Successfully fetched raw email data ({len(raw_email_bytes)} bytes)")
            else:
                print(f"   ✗ Failed to fetch raw email data")
    else:
        print("No messages found to process.")
    
    print("\nEmail Ingestion & Filtering Module test completed.")