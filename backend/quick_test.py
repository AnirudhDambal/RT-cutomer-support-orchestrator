#!/usr/bin/env python3
"""
Quick Test - Fast check of critical components
"""
import os
from pathlib import Path

print("🔍 Quick Setup Check\n")

# 1. Check .env file
env_exists = Path(".env").exists()
print(f"{'✓' if env_exists else '✗'} .env file: {'Found' if env_exists else 'NOT FOUND'}")

if env_exists:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Check for placeholder keys
    placeholder_keys = [
        "your_google_api_key_here",
        "your_api_key_here",
        "your_key_here",
        "your_actual_key_here",
        "your_key",
    ]
    
    if not api_key:
        print("  └─ ✗ API key is empty")
        print("\n❌ REQUIRED: Add your Google API key to .env file")
        print("   1. Get key from: https://makersuite.google.com/app/apikey")
        print("   2. Edit .env file and replace placeholder with your actual key")
        exit(1)
    elif api_key in placeholder_keys or "your" in api_key.lower():
        print(f"  └─ ✗ Placeholder API key detected: {api_key}")
        print("\n❌ REQUIRED: Replace placeholder with your REAL Google API key")
        print("   1. Get key from: https://makersuite.google.com/app/apikey")
        print("   2. Edit .env file:")
        print("      nano .env")
        print("   3. Replace with: GOOGLE_API_KEY=AIzaSy... (your real key)")
        exit(1)
    elif not api_key.startswith("AIza"):
        print(f"  └─ ✗ Invalid API key format (should start with 'AIza')")
        print("\n❌ Check your API key - Google API keys start with 'AIza'")
        exit(1)
    else:
        masked = api_key[:10] + "..." + api_key[-4:]
        print(f"  └─ API Key: {masked}")

# 2. Check knowledge folder
knowledge_path = Path("../knowledge")
txt_files = list(knowledge_path.glob("*.txt")) if knowledge_path.exists() else []
print(f"{'✓' if txt_files else '✗'} Knowledge base: {len(txt_files)} documents")

# 3. Test imports
print("\n📦 Testing imports...")
try:
    import fastapi
    import langchain
    import langgraph
    from langchain_openai import ChatOpenAI
    print("✓ All packages installed")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\n❌ Fix: pip install -r requirements.txt")
    exit(1)

# 4. Quick API test
print("\n🌐 Testing Google Gemini API...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-pro", max_output_tokens=10)
    response = llm.invoke("Hi")
    print(f"✓ API works! Response: {response.content}")
except Exception as e:
    print(f"✗ API test failed: {e}")
    exit(1)

print("\n✅ All critical checks passed! Ready to start backend.")
print("\nRun: python main.py")

