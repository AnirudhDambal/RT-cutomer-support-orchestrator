#!/usr/bin/env python3
"""
Quick test to verify the model is working
"""

import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

def test_model():
    try:
        from config import settings
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        print("🧪 Testing gemini-2.5-flash...")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,
            google_api_key=settings.google_api_key
        )

        start = time.time()
        response = llm.invoke([HumanMessage(content="Say 'Hello World'")])
        elapsed = time.time() - start
        print(f"✅ SUCCESS: {response.content} (Response time: {elapsed:.2f}s)")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_model()
