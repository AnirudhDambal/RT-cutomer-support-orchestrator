# 🔑 Environment Setup Guide

## Quick Setup

### Step 1: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy your API key (starts with `sk-proj-...` or `sk-...`)

### Step 2: Create .env File

**Navigate to backend folder:**
```bash
cd backend
```

**Choose one method:**

#### Method 1: Copy from Example (Recommended)
```bash
# Copy the example file
cp env.example.txt .env

# Edit the file (use your preferred editor)
nano .env
# or
vim .env
# or
code .env
```

Then replace `your_openai_api_key_here` with your actual API key.

#### Method 2: Create Directly (macOS/Linux)
```bash
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

#### Method 3: Create Directly (Windows PowerShell)
```powershell
Set-Content -Path .env -Value "OPENAI_API_KEY=sk-your-actual-key-here"
```

#### Method 4: Create Directly (Windows CMD)
```cmd
echo OPENAI_API_KEY=sk-your-actual-key-here > .env
```

### Step 3: Verify Your .env File

**Check it exists:**
```bash
cat .env
```

**Should look like:**
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Complete .env File Template

If you want to customize all settings, create a `.env` file with:

```env
# REQUIRED: Your OpenAI API Key
OPENAI_API_KEY=sk-your-actual-key-here

# OPTIONAL: Knowledge base path (default: ../knowledge)
KNOWLEDGE_PATH=../knowledge

# OPTIONAL: ChromaDB storage path (default: ./chroma_db)
CHROMA_DB_PATH=./chroma_db
```

---

## Environment Variables Explained

### OPENAI_API_KEY (Required)
- **Purpose**: Authenticate with OpenAI's API to use GPT-4
- **Format**: `sk-proj-...` or `sk-...` (48+ characters)
- **Where to get**: https://platform.openai.com/api-keys
- **Cost**: Pay-per-use (see OpenAI pricing)

### KNOWLEDGE_PATH (Optional)
- **Purpose**: Location of knowledge base documents
- **Default**: `../knowledge` (relative to backend folder)
- **Custom example**: `/path/to/your/knowledge/docs`

### CHROMA_DB_PATH (Optional)
- **Purpose**: Where to store the vector database
- **Default**: `./chroma_db` (in backend folder)
- **Custom example**: `/path/to/vector/db`

---

## For Docker Deployment

If using `docker-compose`, create `.env` in the **project root** (not backend folder):

```bash
# In project root directory
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

Then run:
```bash
docker-compose up -d
```

---

## Security Best Practices

### ✅ DO:
- Keep `.env` file in `.gitignore` (already configured)
- Use environment-specific keys (dev/staging/prod)
- Rotate keys periodically
- Use read-only permissions: `chmod 600 .env`

### ❌ DON'T:
- Commit `.env` to git
- Share your API key publicly
- Hardcode keys in source code
- Use production keys in development

---

## Troubleshooting

### Error: "OpenAI API key not found"

**Check 1:** File exists
```bash
ls -la backend/.env
```

**Check 2:** File has content
```bash
cat backend/.env
```

**Check 3:** Key format is correct
- Should start with `sk-` or `sk-proj-`
- No extra spaces or quotes
- No line breaks in the middle

**Fix:**
```bash
cd backend
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Error: "Invalid API key"

- Verify key is correct (copy-paste from OpenAI dashboard)
- Check key hasn't been revoked
- Ensure you have API credits available
- Try creating a new key

### Error: "Module 'dotenv' not found"

```bash
cd backend
pip install python-dotenv
```

---

## Example Setup Session

Here's a complete example of setting up from scratch:

```bash
# 1. Navigate to project
cd RT-cutomer-support-orchestrator

# 2. Go to backend
cd backend

# 3. Create .env file
echo "OPENAI_API_KEY=sk-proj-abc123..." > .env

# 4. Verify it worked
cat .env

# 5. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run the backend
python main.py
```

You should see:
```
Loaded 5 documents with X chunks into vector store
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Create .env | `echo "OPENAI_API_KEY=sk-..." > .env` |
| View .env | `cat .env` |
| Edit .env | `nano .env` |
| Delete .env | `rm .env` |
| Test backend | `python main.py` |

---

## Need Help?

- **OpenAI API Keys**: https://platform.openai.com/api-keys
- **OpenAI Pricing**: https://openai.com/pricing
- **Project Setup**: See `QUICKSTART.md`
- **Full Documentation**: See `SETUP.md`

---

**Once your .env file is configured, you're ready to run the application! 🚀**

