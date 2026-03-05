"""
Vercel serverless function entry point.
This file imports and exposes the Flask app for Vercel to use.
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel will use this as the entry point
