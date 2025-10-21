#!/usr/bin/env python3
"""
Test the API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8888"

print("🧪 Testing Customer Support API\n")

# Test 1: Root endpoint
print("1️⃣ Testing root endpoint (GET /)...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ Root endpoint works!\n")
except requests.exceptions.ConnectionError:
    print("   ❌ Backend not running! Start it with: python main.py\n")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 2: Query endpoint
print("2️⃣ Testing /query endpoint (POST)...")
try:
    payload = {
        "query": "What is your return policy?"
    }
    response = requests.post(f"{BASE_URL}/query", json=payload)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {data['response'][:100]}...")
        print(f"   Session ID: {data['session_id']}")
        print(f"   Escalation needed: {data['escalation_needed']}")
        print("   ✅ Query endpoint works!\n")
    else:
        print(f"   Response: {response.text}")
        print("   ❌ Query failed\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 3: Another query
print("3️⃣ Testing another query...")
try:
    payload = {
        "query": "How long does shipping take?"
    }
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {data['response'][:100]}...")
        print("   ✅ Second query works!\n")
    else:
        print(f"   ❌ Failed: {response.text}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("="*60)
print("✅ API Testing Complete!")
print("="*60)
print("\n📌 To use the API:")
print("   curl -X POST http://localhost:8000/query \\")
print("        -H 'Content-Type: application/json' \\")
print("        -d '{\"query\": \"Your question here\"}'")
print("\n📖 API Docs: http://localhost:8000/docs")

