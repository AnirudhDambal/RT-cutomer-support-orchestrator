#!/usr/bin/env python3
"""
Test Google API Key Functionality
Tests if the Google API key is working with Gemini models
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_google_api_key():
    """Test if Google API key is working"""
    print("🔍 Testing Google API Key...")
    print("=" * 50)
    
    try:
        # Import required modules
        from config import settings
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        print(f"✅ Config loaded successfully")
        print(f"📝 API Key: {settings.google_api_key[:10]}...{settings.google_api_key[-4:]}")
        print()
        
        # Test 1: Check if API key is set
        if not settings.google_api_key or settings.google_api_key == "your-google-api-key-here":
            print("❌ API Key Error: No valid API key found")
            print("   Please set GOOGLE_API_KEY in your .env file")
            return False
            
        print("✅ API Key is set")
        
        # Test 2: Initialize the model
        print("🤖 Testing model initialization...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=settings.google_api_key
        )
        print("✅ Model initialized successfully")
        
        # Test 3: Make a simple API call
        print("🌐 Testing API call...")
        test_message = HumanMessage(content="Hello! Please respond with 'API test successful'")
        
        try:
            response = llm.invoke([test_message])
            print(f"✅ API Response: {response.content}")
            print()
            print("🎉 SUCCESS: Google API key is working perfectly!")
            return True
            
        except Exception as api_error:
            print(f"❌ API Call Failed: {api_error}")
            
            # Check for specific error types
            if "404" in str(api_error):
                print("   💡 This might be a model availability issue")
                print("   Try using 'gemini-1.5-flash' instead")
            elif "401" in str(api_error) or "403" in str(api_error):
                print("   💡 API key might be invalid or expired")
                print("   Check your key at: https://makersuite.google.com/app/apikey")
            elif "quota" in str(api_error).lower():
                print("   💡 API quota exceeded")
                print("   Check your usage at: https://console.cloud.google.com/")
            
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_alternative_models():
    """Test alternative Gemini models"""
    print("\n🔄 Testing Alternative Models...")
    print("=" * 50)
    
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-pro", 
        "gemini-1.0-pro"
    ]
    
    from config import settings
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
    
    for model in models_to_test:
        try:
            print(f"🧪 Testing {model}...")
            llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=0.1,
                google_api_key=settings.google_api_key
            )
            
            response = llm.invoke([HumanMessage(content="Say 'OK'")])
            print(f"✅ {model}: {response.content}")
            
        except Exception as e:
            print(f"❌ {model}: {str(e)[:100]}...")

def main():
    """Main test function"""
    print("🚀 Google API Key Test Suite")
    print("=" * 50)
    
    # Test main API key
    success = test_google_api_key()
    
    if not success:
        print("\n🔄 Trying alternative models...")
        test_alternative_models()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your API key is working!")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\n💡 Troubleshooting:")
        print("1. Verify your API key at: https://makersuite.google.com/app/apikey")
        print("2. Check your .env file has: GOOGLE_API_KEY=your-key-here")
        print("3. Make sure you have internet connection")
        print("4. Try a different model name")

if __name__ == "__main__":
    main()
