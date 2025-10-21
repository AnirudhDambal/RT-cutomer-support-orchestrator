# 🔧 How to Fix Test Failures

## Common Test Failures & Solutions

---

### ❌ Issue: "Placeholder API key detected"

**Error Message:**
```
✗ Placeholder API key detected: sk-your-actual-api-key-here
❌ REQUIRED: Replace placeholder with your REAL OpenAI API key
```

**Problem:** You haven't set your real OpenAI API key yet.

**Solution - Option 1: Interactive Setup (Easiest)**
```bash
cd backend
source venv/bin/activate
python setup_env.py
```
Follow the prompts to enter your API key.

**Solution - Option 2: Manual Edit**
```bash
cd backend
nano .env  # or use your preferred editor
```
Replace the placeholder with your actual API key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Solution - Option 3: Command Line**
```bash
cd backend
echo "OPENAI_API_KEY=sk-proj-your-real-key-here" > .env
```

**Where to get your API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-` or `sk-proj-`)
5. Paste it in your `.env` file

---

### ❌ Issue: ".env file NOT FOUND"

**Error Message:**
```
✗ .env file: NOT FOUND
```

**Solution:**
```bash
cd backend
python setup_env.py
# OR manually:
echo "OPENAI_API_KEY=your_real_key_here" > .env
```

---

### ❌ Issue: "API test failed: 401 - Incorrect API key"

**Error Message:**
```
✗ API test failed: Error code: 401 - Incorrect API key provided
```

**Possible Causes:**
1. API key is a placeholder (not real)
2. API key was typed incorrectly
3. API key has been revoked
4. Wrong API key (e.g., from different service)

**Solution:**
```bash
# Verify your current key
cat backend/.env

# If it's wrong, get a new one from OpenAI
# Then run interactive setup:
cd backend
python setup_env.py
```

---

### ❌ Issue: "Package NOT installed"

**Error Message:**
```
✗ FastAPI NOT installed
✗ Import error: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

If that doesn't work:
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### ❌ Issue: "Knowledge folder not found"

**Error Message:**
```
✗ Knowledge base: 0 documents
```

**Solution:**
The knowledge folder should be at `../knowledge` relative to the backend folder.

**Verify:**
```bash
ls -la ../knowledge
```

Should show:
- return_policy.txt
- shipping_policy.txt
- faq.txt
- product_info.txt
- privacy_policy.txt

**If missing, check you're in the right location:**
```bash
pwd
# Should be: /path/to/RT-cutomer-support-orchestrator/backend
```

---

### ❌ Issue: "Invalid API key format"

**Error Message:**
```
✗ Invalid API key format (should start with 'sk-')
```

**Solution:**
OpenAI API keys always start with `sk-` (older keys) or `sk-proj-` (newer project keys).

If your key doesn't start with this, you may have:
- Copied the wrong key
- Pasted an Azure or other service key
- Added extra characters

**Fix:**
```bash
cd backend
nano .env
```
Make sure the line looks like:
```
OPENAI_API_KEY=sk-proj-AbCdEf...
```
(no quotes, no spaces, just the key)

---

### ❌ Issue: "OpenAI API connection failed"

**Error Message:**
```
✗ OpenAI API connection failed: Connection timeout
```

**Possible Causes:**
1. No internet connection
2. Firewall blocking OpenAI API
3. VPN/proxy issues
4. OpenAI service is down

**Solution:**
```bash
# Test internet connection
curl https://api.openai.com/v1/models

# If that works but test fails, try:
cd backend
source venv/bin/activate
pip install --upgrade openai langchain-openai
```

---

### ❌ Issue: "ChromaDB/Vector database error"

**Error Message:**
```
✗ Vector database test failed
```

**Solution:**
```bash
# Delete and rebuild vector DB
cd backend
rm -rf chroma_db
python quick_test.py
```

---

## 🚀 Complete Fix Process

If you're having multiple issues, follow this complete reset process:

### 1. Clean Setup
```bash
cd /Users/vadirajdeshpande/RT-cutomer-support-orchestrator/backend

# Clean old files
rm -rf venv chroma_db __pycache__

# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Interactive setup
python setup_env.py

# OR manual
nano .env
# Add: OPENAI_API_KEY=sk-proj-your-real-key
```

### 3. Run Tests
```bash
# Quick test
python quick_test.py

# If that passes, run comprehensive test
python test_setup.py
```

### 4. Start Backend
```bash
# If all tests pass
python main.py
```

---

## 📋 Pre-flight Checklist

Before running tests, verify:

- [ ] You're in the `backend` folder
- [ ] Virtual environment is activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] `.env` file exists (`ls -la .env`)
- [ ] Real API key in `.env` (not placeholder)
- [ ] Knowledge folder exists (`ls -la ../knowledge`)
- [ ] Internet connection working

---

## 🆘 Still Having Issues?

### Get Detailed Diagnostics
```bash
cd backend
source venv/bin/activate
python test_setup.py
```

This will show exactly which component is failing.

### Check Versions
```bash
python --version  # Should be 3.9+
pip list | grep -E "(langchain|fastapi|openai)"
```

### Review Logs
```bash
# Check if there are any error logs
ls -la *.log

# Run with verbose output
python -v quick_test.py
```

---

## 💡 Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| No API key | `python setup_env.py` |
| Wrong API key | Edit `.env`, get new key from OpenAI |
| No packages | `pip install -r requirements.txt` |
| No venv | `python3 -m venv venv && source venv/bin/activate` |
| Corrupt DB | `rm -rf chroma_db` |
| All broken | Follow "Complete Fix Process" above |

---

**After fixing, always re-run the tests:**
```bash
python quick_test.py
```

✅ **When all tests pass, you're ready to start the backend!**

