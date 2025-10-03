# Install required packages:
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# SECURITY REMINDER: Add credentials.json and token.json to .gitignore
# These files contain sensitive authentication information and should never be committed to version control

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the API scope for full email access
SCOPES = ['https://mail.google.com/']

def get_gmail_service():
    """
    Authenticates and returns a Gmail API service object.
    Handles OAuth 2.0 flow, token refresh, and service creation.
    """
    creds = None
    # Check for existing token.json file
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If credentials don't exist or are invalid, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials
            creds.refresh(Request())
        else:
            # Start the OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        # Build and return the Gmail API service object
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == '__main__':
    # Test the authentication and make a simple API call
    service = get_gmail_service()
    if service:
        try:
            # Get the user's profile to confirm authentication
            profile = service.users().getProfile(userId='me').execute()
            print(f'Successfully authenticated! User email: {profile["emailAddress"]}')
        except HttpError as error:
            print(f'An error occurred during the test API call: {error}')
    else:
        print('Failed to authenticate and create Gmail service.')