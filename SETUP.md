# Setup Guide - Customer Support Orchestrator

Complete guide to set up and run the Customer Support Orchestrator system.

## Prerequisites

### Required Software
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Git

### Required API Keys
- OpenAI API key (get from https://platform.openai.com/api-keys)

## Quick Start

### 1. Clone or Navigate to Project

```bash
cd RT-cutomer-support-orchestrator
```

### 2. Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
KNOWLEDGE_PATH=../knowledge
CHROMA_DB_PATH=./chroma_db
EOF

# Edit .env and add your actual OpenAI API key
# Use nano, vim, or any text editor:
nano .env
```

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend folder
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
```

### 5. Access the Application

Open your browser and go to: `http://localhost:3000`

## Detailed Setup

### Backend Configuration

The backend uses several environment variables:

```env
# Required
OPENAI_API_KEY=sk-...  # Your OpenAI API key

# Optional (defaults shown)
KNOWLEDGE_PATH=../knowledge  # Path to knowledge documents
CHROMA_DB_PATH=./chroma_db   # Vector database storage
```

### Knowledge Base Setup

The knowledge base is located in the `knowledge/` folder. It includes:

- `return_policy.txt` - Return and refund information
- `shipping_policy.txt` - Shipping and delivery details
- `faq.txt` - Frequently asked questions
- `product_info.txt` - Product specifications and troubleshooting
- `privacy_policy.txt` - Privacy and security policies

**To add more knowledge:**
1. Create new `.txt` files in the `knowledge/` folder
2. Restart the backend server
3. The system will automatically index the new documents

### Testing the System

#### Test the Backend API

```bash
# Check if backend is running
curl http://localhost:8000

# Test query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'
```

#### Test the Frontend

1. Open `http://localhost:3000`
2. Type a message: "What is your return policy?"
3. You should receive a response from the AI

### Sample Questions to Try

- "What is your return policy?"
- "How can I track my order?"
- "What shipping options do you offer?"
- "Tell me about the Premium Wireless Headphones"
- "I want to return a defective product"
- "How long does shipping take?"

## Architecture Overview

```
┌─────────────────┐
│   React UI      │ (Port 3000)
│   Frontend      │
└────────┬────────┘
         │ HTTP/WebSocket
         ↓
┌─────────────────┐
│   FastAPI       │ (Port 8000)
│   Backend       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  LangGraph      │
│  Supervisor     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ↓         ↓          ↓
┌────────┐ ┌────────┐ ┌───────────┐
│Knowledge│ │Response│ │Escalation │
│ Worker │ │ Worker │ │  Worker   │
└───┬────┘ └────────┘ └───────────┘
    │
    ↓
┌─────────────────┐
│  ChromaDB       │
│  Vector Store   │
└─────────────────┘
```

## Customization

### Modify Agent Behavior

Edit `backend/prompts.py` to customize how agents respond:

```python
SUPERVISOR_PROMPT = """Your custom supervisor instructions..."""
KNOWLEDGE_WORKER_PROMPT = """Your custom knowledge worker..."""
RESPONSE_WORKER_PROMPT = """Your custom response style..."""
ESCALATION_WORKER_PROMPT = """Your custom escalation logic..."""
```

### Change AI Model

Edit `backend/agents.py`:

```python
self.llm = ChatOpenAI(
    model="gpt-4-turbo-preview",  # or gpt-3.5-turbo for cheaper
    temperature=0.7,
    openai_api_key=settings.openai_api_key
)
```

### Customize UI

Edit `frontend/src/App.css` for styling changes.
Edit `frontend/src/App.jsx` for functionality changes.

## Troubleshooting

### Backend Issues

**Error: "No module named 'langchain'"**
```bash
pip install -r requirements.txt
```

**Error: "ChromaDB not found"**
- The vector DB is created on first run
- Delete `chroma_db/` folder and restart if corrupted

**Error: "OpenAI API key not found"**
- Check your `.env` file exists in `backend/`
- Verify the API key is correct
- Ensure no extra spaces or quotes around the key

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check console for CORS errors
- Verify API_BASE_URL in App.jsx

**Error: "npm install fails"**
```bash
rm -rf node_modules package-lock.json
npm install
```

### General Issues

**Slow responses:**
- First query initializes the knowledge base (takes longer)
- Subsequent queries should be faster
- Consider using gpt-3.5-turbo for faster responses

**Memory issues:**
- Large knowledge bases may require more RAM
- Consider splitting documents into smaller files
- Adjust chunk_size in agents.py

## Production Deployment

### Backend

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build for production
npm run build

# Serve with a static server
npm install -g serve
serve -s dist -l 3000
```

### Docker (Optional)

Create `Dockerfile` for backend and frontend, then:

```bash
docker-compose up
```

## Support

For issues or questions:
- Check the README files in backend/ and frontend/
- Review the code comments in agents.py and App.jsx
- Test with sample queries provided above

## Next Steps

1. ✅ Test the basic functionality
2. ✅ Add your own knowledge documents
3. ✅ Customize agent prompts
4. ✅ Modify the UI to match your brand
5. ✅ Deploy to production
6. ✅ Monitor and improve based on user feedback

