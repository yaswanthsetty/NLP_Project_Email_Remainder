#!/usr/bin/env python3
"""
Streamlit App Launcher Script

This script installs Streamlit if not available and launches the dashboard.
"""

import subprocess
import sys
import os

def install_streamlit():
    """Install Streamlit if not available."""
    try:
        import streamlit
        print("✅ Streamlit is already installed")
        return True
    except ImportError:
        print("📦 Installing Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
            print("✅ Streamlit installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Streamlit: {e}")
            return False

def launch_app():
    """Launch the Streamlit application."""
    if install_streamlit():
        print("🚀 Launching Smart Email Reminder Dashboard...")
        print("📱 The app will open in your default web browser")
        print("🔗 URL: http://localhost:8501")
        print("\n💡 To stop the app, press Ctrl+C in this terminal")
        
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        except KeyboardInterrupt:
            print("\n👋 App stopped. Goodbye!")
        except Exception as e:
            print(f"❌ Error launching app: {e}")
    else:
        print("❌ Cannot launch app without Streamlit")

if __name__ == "__main__":
    launch_app()