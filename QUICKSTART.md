# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Prerequisites
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- OpenAI API Key ([Get Here](https://platform.openai.com/api-keys))

### Step 2: Clone/Navigate to Project
```bash
cd RT-cutomer-support-orchestrator
```

### Step 3: Configure Environment
```bash
# Create .env file in backend folder
cd backend
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
cd ..
```

### Step 4: Run the App

**Option A: Use Start Script (Recommended)**

macOS/Linux:
```bash
./start.sh
```

Windows:
```bash
start.bat
```

**Option B: Manual Start**

Terminal 1 - Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm run dev
```

### Step 5: Open the App
Go to: **http://localhost:3000**

---

## 🎯 Try These Questions

Once the app is running, try asking:

1. **"What is your return policy?"**
   - Tests knowledge retrieval from return_policy.txt

2. **"How can I track my order?"**
   - Tests FAQ knowledge retrieval

3. **"Tell me about the Premium Wireless Headphones"**
   - Tests product information retrieval

4. **"I want to return a defective product"**
   - Tests escalation worker

5. **"What shipping options do you offer?"**
   - Tests shipping policy retrieval

---

## 📁 Project Structure

```
RT-cutomer-support-orchestrator/
├── backend/              # Python FastAPI + LangGraph
├── frontend/             # React chat interface
├── knowledge/            # Knowledge base documents
├── start.sh / start.bat  # Quick start scripts
├── README.md            # Full documentation
├── SETUP.md             # Detailed setup guide
└── ARCHITECTURE.md      # Technical architecture
```

---

## 🛠️ Common Issues

**"Backend won't start"**
```bash
# Check your .env file
cat backend/.env

# Should contain:
# OPENAI_API_KEY=sk-...
```

**"Frontend can't connect"**
```bash
# Make sure backend is running on port 8000
curl http://localhost:8000
```

**"Slow first response"**
- First query loads the knowledge base (takes 3-5 seconds)
- Subsequent queries are much faster!

---

## 📚 What's Included

### Backend (LangGraph + FastAPI)
✅ Supervisor Agent
✅ 3 Worker Agents (Knowledge, Response, Escalation)
✅ ChromaDB Vector Database
✅ REST API + WebSocket
✅ Session Management

### Frontend (React)
✅ Beautiful Chat UI
✅ Real-time messaging
✅ Quick question shortcuts
✅ Session management
✅ Responsive design

### Knowledge Base
✅ Return Policy
✅ Shipping Policy
✅ FAQ (50+ questions)
✅ Product Information
✅ Privacy Policy

---

## 🎨 Customization

**Add Your Own Knowledge:**
1. Create `.txt` file in `knowledge/` folder
2. Restart backend
3. Done! Automatically indexed

**Change Agent Prompts:**
Edit `backend/prompts.py`

**Modify UI:**
Edit `frontend/src/App.css`

---

## 🐳 Docker Deployment

```bash
# Create .env file
echo "OPENAI_API_KEY=your_key" > .env

# Start with Docker Compose
docker-compose up -d

# Access at http://localhost:3000
```

---

## 📞 Support

- 📖 Full docs: See [README.md](README.md)
- 🔧 Setup help: See [SETUP.md](SETUP.md)
- 🏗️ Architecture: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## ✅ Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key obtained
- [ ] .env file created with API key
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Tested with sample questions

---

**Once everything is checked, you're ready to go! 🎉**

