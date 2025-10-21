# 🧪 Testing Tools Reference

Quick reference for all backend testing and setup tools.

---

## 🚀 Setup & Configuration

### `setup_env.py` - Interactive API Key Setup ⭐
**Use this first if you haven't set up your API key**

```bash
python setup_env.py
```

**What it does:**
- Prompts for your OpenAI API key
- Validates format and length
- Creates/updates .env file
- Verifies configuration
- Shows masked key for security

**When to use:**
- First-time setup
- Updating API key
- If .env is missing or invalid

---

## ✅ Testing Scripts

### `quick_test.py` - Fast Validation (10 seconds) ⚡
**Use this before starting the backend**

```bash
python quick_test.py
```

**What it checks:**
1. ✓ .env file exists
2. ✓ API key is valid (not placeholder)
3. ✓ Knowledge base has documents
4. ✓ Required packages installed
5. ✓ OpenAI API connection works

**Exit codes:**
- `0` - All tests passed ✅
- `1` - One or more tests failed ❌

---

### `test_setup.py` - Comprehensive Diagnostics (30-60 seconds) 🔬
**Use this for detailed troubleshooting**

```bash
python test_setup.py
```

**What it tests:**
1. Package imports (all dependencies)
2. Environment configuration
3. OpenAI API connection
4. Knowledge base folder & files
5. Vector database initialization
6. Document loading & chunking
7. Configuration module

**Output:** Detailed report with PASS/FAIL for each component

---

## 📚 Documentation

### `FIX_TESTS.md` - Troubleshooting Guide
Solutions for every possible test failure

### `TEST_GUIDE.md` - Testing Documentation
Complete guide to using test scripts

### `TESTS_FIXED.md` - Recent Improvements
Summary of fixes and current status

### `TESTING_TOOLS.md` - This File
Quick reference for all tools

---

## 🎯 Common Workflows

### First-Time Setup
```bash
# 1. Setup API key
python setup_env.py

# 2. Verify setup
python quick_test.py

# 3. Start backend
python main.py
```

### Before Each Backend Start
```bash
# Quick check
python quick_test.py

# If pass, start
python main.py
```

### When Tests Fail
```bash
# Get detailed diagnostics
python test_setup.py

# Read solutions
cat FIX_TESTS.md

# Re-run quick test
python quick_test.py
```

### Update API Key
```bash
# Interactive update
python setup_env.py

# Or manual edit
nano .env

# Verify
python quick_test.py
```

---

## 📊 Test Comparison

| Script | Speed | Detail | Use Case |
|--------|-------|--------|----------|
| `quick_test.py` | ⚡ Fast (10s) | Basic | Pre-flight check |
| `test_setup.py` | 🐢 Slow (60s) | Detailed | Troubleshooting |
| `setup_env.py` | ⚡ Fast (1min) | N/A | Configuration |

---

## 🎨 Output Examples

### ✅ Successful Quick Test
```
🔍 Quick Setup Check

✓ .env file: Found
  └─ API Key: sk-proj-AB...xyz
✓ Knowledge base: 5 documents

📦 Testing imports...
✓ All packages installed

🌐 Testing OpenAI API...
✓ API works! Response: Hello

✅ All critical checks passed! Ready to start backend.

Run: python main.py
```

### ❌ Failed Quick Test (Placeholder Key)
```
🔍 Quick Setup Check

✓ .env file: Found
  └─ ✗ Placeholder API key detected: sk-your-actual-api-key-here

❌ REQUIRED: Replace placeholder with your REAL OpenAI API key
   1. Get key from: https://platform.openai.com/api-keys
   2. Edit .env file:
      nano .env
   3. Replace with: OPENAI_API_KEY=sk-proj-xxxxx...
```

### ✅ Successful Setup
```
============================================================
   🔑 OpenAI API Key Setup
============================================================

📝 You need an OpenAI API key to use this application.

Get your API key from:
   👉 https://platform.openai.com/api-keys

Enter your OpenAI API key: sk-proj-abc123...

✓ Key received: sk-proj-ab...xyz
  Is this correct? (y/n): y

✅ .env file created successfully!
   Location: /path/to/backend/.env

============================================================
   🔍 Verifying Setup
============================================================

✓ API Key loaded: sk-proj-ab...xyz
✓ Configuration valid!

============================================================
   ✅ Setup Complete!
============================================================

Next steps:
   1. Run tests: python quick_test.py
   2. Start backend: python main.py
```

---

## 🔍 What Gets Tested

### Environment
- [x] .env file exists
- [x] OPENAI_API_KEY is set
- [x] API key format valid (starts with `sk-`)
- [x] API key not a placeholder
- [x] API key length sufficient

### Dependencies
- [x] fastapi
- [x] uvicorn
- [x] langchain
- [x] langgraph
- [x] langchain-openai
- [x] langchain-community
- [x] chromadb
- [x] sentence-transformers
- [x] python-dotenv

### Knowledge Base
- [x] ../knowledge folder exists
- [x] Contains .txt files
- [x] Files are readable
- [x] Documents load successfully
- [x] Text chunking works

### AI Components
- [x] OpenAI API connection
- [x] Embedding model loads
- [x] Vector database initializes
- [x] Document retrieval works

### Configuration
- [x] config.py loads
- [x] Settings are valid
- [x] Paths are correct

---

## 💡 Tips

1. **Always run quick_test.py before starting backend**
   - Catches issues early
   - Saves debugging time
   - Verifies API connectivity

2. **Use setup_env.py for first-time setup**
   - Validates your input
   - Prevents common mistakes
   - Guides you through process

3. **Run test_setup.py when troubleshooting**
   - Shows exactly what's failing
   - Provides detailed diagnostics
   - Helps identify root cause

4. **Check FIX_TESTS.md for solutions**
   - Every error has a fix
   - Step-by-step instructions
   - Common issues covered

---

## 🔗 Quick Commands

```bash
# Setup
python setup_env.py                    # Configure API key

# Testing  
python quick_test.py                   # Fast check
python test_setup.py                   # Full diagnostics

# Verification
cat .env                               # View config
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY')[:10])"  # Check key

# Running
python main.py                         # Start backend
```

---

## 📞 Support Files

| File | Purpose |
|------|---------|
| `env.example.txt` | Template for .env file |
| `FIX_TESTS.md` | Troubleshooting solutions |
| `TEST_GUIDE.md` | Complete testing guide |
| `TESTS_FIXED.md` | Recent improvements |
| `TESTING_TOOLS.md` | This reference |

---

**Pro Tip:** Bookmark this file for quick reference! 🔖

