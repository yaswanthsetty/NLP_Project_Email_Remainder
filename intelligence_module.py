"""
Intelligence & NLP Module for Smart Email Reminder System

This module analyzes clean email text to identify actionable events like deadlines and meetings.
Uses a hybrid approach: spaCy for Named Entity Recognition (NER) and dateparser for robust date parsing.

Required packages:
pip install spacy dateparser

Required spaCy model:
python -m spacy download en_core_web_sm
"""

import spacy
import dateparser
from datetime import datetime
from typing import List, Dict, Optional, Any


def find_actionable_events(text: str) -> List[Dict[str, Any]]:
    """
    Analyze email text to identify actionable events like deadlines and meetings.
    
    Uses spaCy for Named Entity Recognition to find dates in context,
    then dateparser to convert findings into proper datetime objects.
    
    Args:
        text: Clean email body text to analyze
        
    Returns:
        List of dictionaries containing actionable events with context and datetime objects
    """
    if not text or not text.strip():
        return []
    
    try:
        # Load the pre-trained spaCy model
        nlp = spacy.load('en_core_web_sm')
        
        # Process the input text with spaCy
        doc = nlp(text)
        
        # Store potential events found by spaCy NER
        potential_events = []
        
        # Iterate through named entities to find dates and times
        for ent in doc.ents:
            if ent.label_ in ['DATE', 'TIME']:
                # Find context by getting the grammatical "head" of the entity's root token
                # This often captures key verbs/nouns like "due", "meeting", "schedule"
                context_word = ent.root.head.text
                
                # Get surrounding context for better understanding
                # Look at tokens before and after the entity
                start_idx = max(0, ent.start - 3)
                end_idx = min(len(doc), ent.end + 3)
                surrounding_context = doc[start_idx:end_idx].text
                
                potential_events.append({
                    'entity_text': ent.text,
                    'entity_label': ent.label_,
                    'context_word': context_word,
                    'surrounding_context': surrounding_context.strip(),
                    'start_char': ent.start_char,
                    'end_char': ent.end_char
                })
        
        # Use dateparser to validate and parse the potential events
        actionable_events = []
        current_time = datetime.now()
        
        for event in potential_events:
            try:
                # Use dateparser with future preference setting
                parsed_datetime = dateparser.parse(
                    event['entity_text'],
                    settings={'PREFER_DATES_FROM': 'future'}
                )
                
                # Check if dateparser returned a valid datetime and it's in the future
                if (parsed_datetime and 
                    isinstance(parsed_datetime, datetime) and 
                    parsed_datetime > current_time):
                    
                    # Create event context from surrounding text and context word
                    event_context = f"{event['context_word']} - {event['surrounding_context']}"
                    
                    actionable_events.append({
                        'event_context': event_context.strip(),
                        'datetime': parsed_datetime,
                        'original_text': event['entity_text'],
                        'entity_label': event['entity_label']
                    })
                    
            except Exception as e:
                print(f"Warning: Could not parse date '{event['entity_text']}': {e}")
                continue
        
        return actionable_events
        
    except OSError as e:
        print(f"Error: Could not load spaCy model. Please install it with: python -m spacy download en_core_web_sm")
        print(f"Error details: {e}")
        return []
    except Exception as e:
        print(f"Error analyzing text for actionable events: {e}")
        return []


def analyze_email_content(parsed_email: Dict[str, str]) -> Dict[str, Any]:
    """
    Comprehensive analysis of parsed email content to extract actionable insights.
    
    Args:
        parsed_email: Dictionary from email_parser with keys: subject, from, to, body
        
    Returns:
        Dictionary containing analysis results and actionable events
    """
    if not parsed_email or 'body' not in parsed_email:
        return {'actionable_events': [], 'analysis_summary': 'No email content to analyze'}
    
    # Combine subject and body for comprehensive analysis
    full_text = f"{parsed_email.get('subject', '')} {parsed_email.get('body', '')}"
    
    # Find actionable events in the combined text
    events = find_actionable_events(full_text)
    
    # Create analysis summary
    analysis_summary = {
        'total_events_found': len(events),
        'email_subject': parsed_email.get('subject', ''),
        'email_from': parsed_email.get('from', ''),
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    return {
        'actionable_events': events,
        'analysis_summary': analysis_summary
    }


if __name__ == '__main__':
    """
    Test the intelligence module with sample email text containing various temporal expressions.
    """
    print("🧠 Testing Intelligence & NLP Module...")
    print("=" * 60)
    
    # Create sample email text with various temporal expressions for testing
    sample_email_text = """
    Hi Team,
    
    I hope this email finds you well. I wanted to follow up on a few important items:
    
    The project report is due next Friday. Please make sure to include all the quarterly metrics 
    and analysis that we discussed in the planning meeting.
    
    Let's schedule the review meeting for October 28th at 2 PM PST. This will give us enough 
    time to review the submissions and prepare feedback.
    
    The meeting on last Monday was very productive and we made significant progress on the 
    Q3 objectives.
    
    Please submit your timesheet by the 5th. HR needs these for payroll processing.
    
    Don't forget that the client presentation is scheduled for next Wednesday at 10 AM.
    
    The conference call with the stakeholders is set for tomorrow at 3 PM EST.
    
    We had a great workshop last week, but let's plan the next one for December 15th.
    
    Best regards,
    Project Manager
    """
    
    print("📧 Sample Email Text:")
    print("-" * 40)
    print(sample_email_text[:300] + "..." if len(sample_email_text) > 300 else sample_email_text)
    print("-" * 40)
    print()
    
    # Test the find_actionable_events function
    print("🔍 Analyzing for actionable events...")
    events = find_actionable_events(sample_email_text)
    
    print("\n--- Found Actionable Events ---")
    
    if events:
        print(f"✅ Found {len(events)} actionable event(s):")
        print()
        
        for i, event in enumerate(events, 1):
            print(f"Event #{i}:")
            print(f"  📅 Date/Time: {event['datetime'].strftime('%A, %B %d, %Y at %I:%M %p')}")
            print(f"  📝 Context: {event['event_context']}")
            print(f"  📄 Original Text: '{event['original_text']}'")
            print(f"  🏷️  Entity Type: {event['entity_label']}")
            
            # Calculate days until event
            days_until = (event['datetime'] - datetime.now()).days
            if days_until == 0:
                print(f"  ⏰ Timing: Today!")
            elif days_until == 1:
                print(f"  ⏰ Timing: Tomorrow")
            else:
                print(f"  ⏰ Timing: {days_until} days from now")
            print()
    else:
        print("❌ No actionable events found in the sample text.")
        print("This could mean:")
        print("  - No future dates/times were detected")
        print("  - spaCy model is not installed (run: python -m spacy download en_core_web_sm)")
        print("  - dateparser could not parse the detected dates")
    
    print("=" * 60)
    print("🧠 Intelligence module testing completed!")
    
    # Test integration with email parser if available
    try:
        print("\n🔗 Testing integration with email parser...")
        from email_parser import parse_raw_email
        
        # Create a mock parsed email for testing
        mock_parsed_email = {
            'subject': 'Project Update - Action Items Due',
            'from': 'manager@company.com',
            'to': 'team@company.com',
            'body': sample_email_text
        }
        
        # Test the comprehensive analysis function
        analysis_result = analyze_email_content(mock_parsed_email)
        
        print("\n📊 Comprehensive Email Analysis:")
        print(f"Subject: {analysis_result['analysis_summary']['email_subject']}")
        print(f"From: {analysis_result['analysis_summary']['email_from']}")
        print(f"Events Found: {analysis_result['analysis_summary']['total_events_found']}")
        print(f"Analysis Time: {analysis_result['analysis_summary']['analysis_timestamp']}")
        
    except ImportError:
        print("Note: email_parser.py not found - skipping integration test")
    except Exception as e:
        print(f"Integration test error: {e}")