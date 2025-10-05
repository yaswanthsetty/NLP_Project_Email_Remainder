#!/usr/bin/env python3
"""
Notification Test Script for Smart Email Reminder System

This script helps verify that the notification system is working properly
on your Windows 11 system.
"""

import sys
import platform
from notifier import send_desktop_notification

def test_notifications():
    """Test the notification system with different scenarios."""

    print("🔔 Smart Email Reminder - Notification Test")
    print("=" * 50)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print()

    # Test 1: Basic notification
    print("Test 1: Basic notification...")
    result1 = send_desktop_notification(
        "Test Notification",
        "This is a basic test notification."
    )
    print(f"Result: {'✅ Success' if result1 else '❌ Failed'}")
    print()

    # Test 2: Reminder-style notification
    print("Test 2: Reminder-style notification...")
    result2 = send_desktop_notification(
        "Meeting Reminder",
        "Team standup meeting in 15 minutes\nLocation: Conference Room A\nAttendees: John, Sarah, Mike"
    )
    print(f"Result: {'✅ Success' if result2 else '❌ Failed'}")
    print()

    # Test 3: Long message notification
    print("Test 3: Long message notification...")
    result3 = send_desktop_notification(
        "Project Deadline Reminder",
        "The quarterly report is due tomorrow at 5:00 PM. Please ensure all sections are completed and reviewed. Key deliverables include: financial summary, project metrics, and future roadmap. Contact your manager if you need extensions."
    )
    print(f"Result: {'✅ Success' if result3 else '❌ Failed'}")
    print()

    print("🎯 Troubleshooting Tips for Windows 11:")
    print("1. Check Windows Settings > System > Notifications & actions")
    print("2. Ensure 'Get notifications from apps and other senders' is ON")
    print("3. Look for 'Smart Email Reminder' in the app list and enable it")
    print("4. Check if Focus Assist (Do Not Disturb) is turned OFF")
    print("5. Try running the script as Administrator")
    print("6. Restart your computer if notifications still don't appear")
    print()

    all_passed = all([result1, result2, result3])
    print(f"Overall Test Result: {'✅ All tests passed!' if all_passed else '❌ Some tests failed'}")

    return all_passed

if __name__ == "__main__":
    test_notifications()