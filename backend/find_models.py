#!/usr/bin/env python3
"""
Find Available Google Gemini Models
"""

import google.generativeai as genai
import os
from pathlib import Path
import sys

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def find_available_models():
    """Find available Gemini models"""
    print("🔍 Finding Available Google Gemini Models...")
    print("=" * 50)
    
    try:
        # Load API key from .env
        from config import settings
        api_key = settings.google_api_key
        
        print(f"📝 Using API Key: {api_key[:10]}...{api_key[-4:]}")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List all available models
        print("\n🤖 Available Models:")
        print("-" * 30)
        
        models = genai.list_models()
        
        for model in models:
            model_name = model.name
            print(f"✅ {model_name}")
            
            # Check if it supports generateContent
            if 'generateContent' in model.supported_generation_methods:
                print(f"   📝 Supports: generateContent")
            else:
                print(f"   ❌ No generateContent support")
        
        print(f"\n📊 Total models found: {len(list(models))}")
        
        # Test a simple model
        print("\n🧪 Testing a simple model...")
        try:
            # Try the first available model
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'Hello World'")
            print(f"✅ Test successful: {response.text}")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_available_models()
