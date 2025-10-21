# Backend Testing Guide

## Quick Test Scripts

Before starting the backend, use these test scripts to verify your setup.

---

## 🚀 Quick Test (Recommended)

**Fast check of critical components (~10 seconds)**

```bash
cd backend
source venv/bin/activate  # If using virtual environment
python quick_test.py
```

**What it checks:**
- ✓ .env file exists
- ✓ OPENAI_API_KEY is set correctly
- ✓ Knowledge base documents exist
- ✓ Required packages installed
- ✓ OpenAI API connection works

**Expected output:**
```
🔍 Quick Setup Check

✓ .env file: Found
  └─ API Key: sk-proj-...xyz
✓ Knowledge base: 5 documents

📦 Testing imports...
✓ All packages installed

🌐 Testing OpenAI API...
✓ API works! Response: Hello

✅ All critical checks passed! Ready to start backend.

Run: python main.py
```

---

## 🔬 Full Test Suite

**Comprehensive test of all components (~30-60 seconds)**

```bash
cd backend
source venv/bin/activate
python test_setup.py
```

**What it tests:**
1. Package imports (FastAPI, LangChain, LangGraph, ChromaDB, etc.)
2. Environment configuration (.env file)
3. OpenAI API connection
4. Knowledge base folder and files
5. Vector database initialization
6. Document loading and chunking
7. Configuration module

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║               BACKEND SETUP TEST SUITE                   ║
╚══════════════════════════════════════════════════════════╝

============================================================
1. Testing Package Imports
============================================================
✓ FastAPI installed
✓ Uvicorn installed
✓ LangChain installed
✓ LangGraph installed
...

============================================================
2. Testing Environment Configuration
============================================================
✓ .env file exists
✓ OPENAI_API_KEY found: sk-proj-...xyz

============================================================
3. Testing OpenAI API Connection
============================================================
ℹ Creating OpenAI client...
ℹ Sending test request...
✓ API Response: OK
✓ OpenAI API connection successful!

============================================================
4. Testing Knowledge Base
============================================================
✓ Knowledge folder found: /path/to/knowledge
✓ Found 5 knowledge documents:
ℹ   - return_policy.txt (2450 bytes)
ℹ   - shipping_policy.txt (1850 bytes)
ℹ   - faq.txt (3200 bytes)
ℹ   - product_info.txt (2900 bytes)
ℹ   - privacy_policy.txt (2750 bytes)

============================================================
5. Testing Vector Database
============================================================
ℹ Loading embedding model (this may take a moment)...
✓ Embedding model loaded successfully
ℹ Generating test embedding...
✓ Embedding generated (dimension: 384)

============================================================
6. Testing Document Loading
============================================================
ℹ Loading documents...
✓ Loaded 5 documents
ℹ Splitting documents into chunks...
✓ Created 42 chunks
ℹ Sample chunk: RETURN AND REFUND POLICY...

============================================================
7. Testing Configuration Module
============================================================
✓ Configuration loaded successfully
ℹ Knowledge Path: ../knowledge
ℹ ChromaDB Path: ./chroma_db
✓ API Key: sk-proj-...xyz

============================================================
TEST SUMMARY
============================================================
✓ IMPORTS: PASS
✓ ENV: PASS
✓ OPENAI: PASS
✓ KNOWLEDGE: PASS
✓ VECTOR_DB: PASS
✓ DOCUMENTS: PASS
✓ CONFIG: PASS

============================================================
Results: 7/7 tests passed
============================================================

🎉 ALL TESTS PASSED! You're ready to start the backend!

Run the backend with:
  python main.py
```

---

## 🔧 Troubleshooting

### Test fails: ".env file NOT found"

**Fix:**
```bash
cd backend
echo "OPENAI_API_KEY=your_actual_key_here" > .env
```

### Test fails: "OPENAI_API_KEY looks invalid"

**Fix:**
1. Get your key from https://platform.openai.com/api-keys
2. Replace in .env file:
```bash
echo "OPENAI_API_KEY=sk-proj-actual-key-here" > .env
```

### Test fails: "Package NOT installed"

**Fix:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Test fails: "OpenAI API connection failed"

**Possible causes:**
- Invalid API key
- No internet connection
- No API credits

**Fix:**
1. Verify API key on OpenAI dashboard
2. Check internet connection
3. Verify account has credits

### Test fails: "Knowledge folder not found"

**Fix:**
```bash
# Knowledge folder should be at: ../knowledge
# Verify it exists:
ls -la ../knowledge

# Should show .txt files
```

---

## 📋 Pre-flight Checklist

Before running the backend, ensure:

- [ ] Virtual environment activated
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid API key
- [ ] Knowledge folder exists with .txt files
- [ ] Quick test passes (`python quick_test.py`)

---

## 🚀 After Tests Pass

Once all tests pass, start the backend:

```bash
python main.py
```

You should see:
```
Loaded 5 documents with 42 chunks into vector store
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then test the API:
```bash
# In another terminal
curl http://localhost:8000/
```

---

## 💡 Tips

1. **Always run quick_test.py first** - It's fast and catches common issues
2. **Use test_setup.py for troubleshooting** - Shows detailed diagnostics
3. **Keep tests green** - If tests pass, backend will likely work
4. **Test after changes** - Re-run tests after modifying code or config

---

## 📊 Test Output Colors

- 🟢 **Green ✓** - Test passed
- 🔴 **Red ✗** - Test failed  
- 🟡 **Yellow ⚠** - Warning
- 🔵 **Blue ℹ** - Information

---

## 🔄 Automation

Add to your workflow:

```bash
#!/bin/bash
# start_with_tests.sh

cd backend
source venv/bin/activate

# Run quick test
if python quick_test.py; then
    echo "Tests passed! Starting backend..."
    python main.py
else
    echo "Tests failed! Fix issues before starting."
    exit 1
fi
```

---

**Happy Testing! 🧪**

