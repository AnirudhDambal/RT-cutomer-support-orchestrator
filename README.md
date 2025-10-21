# 🧠 Real-Time Customer Support Orchestrator with Knowledge-Augmented Responses  
### (Customer Experience using Agentic AI, LangGraph)

## 🚀 Project Overview
This is a **production-ready intelligent customer support system** that uses **LangGraph's Agentic AI** with a supervisor-worker architecture to provide efficient, context-aware, and knowledge-augmented responses.  

The system integrates **LLMs, RAG (Retrieval-Augmented Generation), and conversation memory** to deliver human-like assistance, automate query resolution, and intelligently escalate complex cases.

---

## ✨ Features Implemented

✅ **LangGraph Supervisor-Worker Architecture**
- 1 Supervisor Agent coordinating 3 specialized workers
- Knowledge Worker for RAG-based information retrieval
- Response Worker for customer-friendly answer generation
- Escalation Worker for complex case handling

✅ **Knowledge Base System**
- Vector database (ChromaDB) for semantic search
- Pre-loaded with policies, FAQs, product info
- Automatic document indexing and retrieval

✅ **Modern React Frontend**
- Beautiful gradient UI with smooth animations
- Real-time chat interface
- Session management and history
- Quick question shortcuts
- Escalation indicators

✅ **FastAPI Backend**
- RESTful API endpoints
- WebSocket support for real-time chat
- Session management
- CORS enabled for frontend integration

✅ **Production Ready**
- Docker support with docker-compose
- Complete documentation
- Environment configuration
- Error handling and validation

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                    │
│         (Beautiful Chat UI - Port 3000)            │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/WebSocket
                   ↓
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│           LangGraph Supervisor Agent                │
│      (Coordinates workflow & routing)               │
└──────────┬──────────────┬──────────────┬────────────┘
           │              │              │
    ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼────────┐
    │ Knowledge  │ │  Response  │ │ Escalation  │
    │  Worker    │ │   Worker   │ │   Worker    │
    └──────┬─────┘ └────────────┘ └─────────────┘
           │
           ↓
    ┌─────────────────┐
    │  ChromaDB       │
    │  Vector Store   │
    │  (Knowledge)    │
    └─────────────────┘
```

## 📁 Project Structure

```
RT-cutomer-support-orchestrator/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── agents.py            # LangGraph agent system
│   ├── prompts.py           # Agent prompts (customizable)
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── README.md           # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main chat component
│   │   ├── App.css         # Styling
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── Dockerfile          # Docker configuration
│   ├── nginx.conf          # Nginx configuration
│   └── README.md          # Frontend documentation
├── knowledge/              # Knowledge base documents
│   ├── return_policy.txt
│   ├── shipping_policy.txt
│   ├── faq.txt
│   ├── product_info.txt
│   └── privacy_policy.txt
├── docker-compose.yml      # Docker compose configuration
├── SETUP.md               # Complete setup guide
└── README.md              # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Start backend
python main.py
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Access the App

Open http://localhost:3000 in your browser!

**For detailed setup instructions, see [SETUP.md](SETUP.md)**

---

## 🧠 Agent System Details

### Supervisor Agent
- **Role**: Orchestrates the entire workflow
- **Decisions**: Routes queries to appropriate workers
- **Logic**: Analyzes query complexity and determines worker sequence

### Knowledge Worker
- **Role**: Retrieves relevant information from knowledge base
- **Technology**: ChromaDB for vector similarity search
- **Sources**: Policies, FAQs, product docs (in `/knowledge` folder)
- **Output**: Relevant excerpts with confidence scores

### Response Worker
- **Role**: Generates customer-friendly responses
- **Input**: User query + knowledge from Knowledge Worker
- **Style**: Warm, professional, helpful, concise
- **Context**: Maintains conversation history

### Escalation Worker
- **Role**: Assesses if human intervention is needed
- **Criteria**: Complaints, refunds, complex issues, legal matters
- **Priority Levels**: High/Medium/Low
- **Output**: Escalation recommendation + human agent summary

---

## 🎯 Key Features

### Knowledge Base (RAG)
The system uses **Retrieval-Augmented Generation** with:
- 5 pre-loaded knowledge documents
- Semantic search via embeddings
- Automatic chunking and indexing
- Real-time document retrieval

**Add your own knowledge**: Just drop `.txt` files in the `knowledge/` folder!

### Intelligent Routing
The supervisor intelligently routes queries:
- Policy questions → Knowledge Worker → Response Worker
- Complaints/Refunds → Escalation Worker → Response Worker
- Simple greetings → Response Worker directly

### Session Management
- Unique session IDs for each conversation
- Chat history maintained per session
- Context-aware responses using previous messages
- Clear session functionality

---

## ⚙️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React 18 + Vite | Modern UI with fast builds |
| **Backend** | FastAPI | High-performance async API |
| **Agent Framework** | LangGraph | Orchestrating agent workflows |
| **LLM** | OpenAI GPT-4 | Natural language understanding |
| **Vector DB** | ChromaDB | Semantic search for RAG |
| **Embeddings** | HuggingFace | Document embeddings |
| **Deployment** | Docker + Nginx | Production deployment |

---

## 🎨 Customization

### Modify Agent Behavior
Edit `backend/prompts.py` to customize:
- Supervisor routing logic
- Knowledge retrieval strategy
- Response tone and style
- Escalation criteria

### Add Knowledge Documents
1. Create `.txt` files in `knowledge/` folder
2. Restart backend
3. Documents are automatically indexed!

### Change UI Theme
Edit `frontend/src/App.css`:
```css
/* Change gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## 📊 Sample Queries to Try

- "What is your return policy?"
- "How can I track my order?"
- "What shipping options do you offer?"
- "Tell me about the Premium Wireless Headphones"
- "I want to return a defective product"
- "How long does international shipping take?"
- "What payment methods do you accept?"

---

## 🐳 Docker Deployment

```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Start all services
docker-compose up -d

# Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup and deployment guide
- **[backend/README.md](backend/README.md)** - Backend API documentation
- **[frontend/README.md](frontend/README.md)** - Frontend component guide

---

## 🔧 Troubleshooting

**Backend won't start?**
- Check OpenAI API key in `.env`
- Ensure Python 3.9+ is installed
- Install all dependencies: `pip install -r requirements.txt`

**Frontend can't connect?**
- Verify backend is running on port 8000
- Check CORS settings
- Inspect browser console for errors

**Slow responses?**
- First query initializes knowledge base (slower)
- Consider using GPT-3.5 for faster responses
- Check your OpenAI API rate limits

**See [SETUP.md](SETUP.md) for detailed troubleshooting**

---

## 🎯 What Makes This Special

1. **Production-Ready**: Complete with Docker, error handling, and docs
2. **True Agent System**: LangGraph supervisor-worker pattern, not just LLM chains
3. **RAG Implementation**: Real vector search with ChromaDB
4. **Beautiful UI**: Modern, responsive React interface
5. **Fully Customizable**: Easy to modify prompts, add knowledge, change styling
6. **Context-Aware**: Maintains conversation history and session state
7. **Intelligent Escalation**: Knows when to involve humans

---

## 🚀 Next Steps

1. ✅ Follow [SETUP.md](SETUP.md) to get started
2. ✅ Try the sample queries
3. ✅ Add your own knowledge documents
4. ✅ Customize agent prompts for your use case
5. ✅ Modify UI to match your brand
6. ✅ Deploy to production with Docker

---

## 📝 License

This project is open source and available for educational and commercial use.

---

## 💡 Built With

- **LangGraph** for agent orchestration
- **OpenAI GPT-4** for language understanding
- **ChromaDB** for vector search
- **FastAPI** for high-performance backend
- **React** for modern frontend
- **Docker** for easy deployment

---

**Happy Building! 🎉**
