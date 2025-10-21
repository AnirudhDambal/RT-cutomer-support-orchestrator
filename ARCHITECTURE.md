# System Architecture - Customer Support Orchestrator

## Overview

This document describes the technical architecture of the Customer Support Orchestrator system, built using LangGraph's supervisor-worker pattern.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Browser
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Chat UI    │  │  Session Mgr │  │ Quick Actions │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/WebSocket (Port 3000 → 8000)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  REST API    │  │  WebSocket   │  │  Session DB  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Python Function Calls
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Orchestrator                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Supervisor Agent (GPT-4)                   │  │
│  │  • Analyzes query intent                             │  │
│  │  • Routes to appropriate workers                     │  │
│  │  • Coordinates workflow                              │  │
│  └─────────────────┬────────────────────────────────────┘  │
│                    │                                        │
│         ┌──────────┼──────────┐                             │
│         │          │          │                             │
│    ┌────▼────┐ ┌───▼────┐ ┌──▼──────┐                      │
│    │Knowledge│ │Response│ │Escalation│                      │
│    │ Worker  │ │ Worker │ │  Worker  │                      │
│    └────┬────┘ └────────┘ └──────────┘                      │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          │ Vector Similarity Search
          ↓
┌─────────────────────────────────────────────────────────────┐
│               ChromaDB Vector Database                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Embeddings │  │   Vectors   │  │  Metadata   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Document Storage
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   Knowledge Base Files                      │
│  • return_policy.txt                                        │
│  • shipping_policy.txt                                      │
│  • faq.txt                                                  │
│  • product_info.txt                                         │
│  • privacy_policy.txt                                       │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend Layer (React + Vite)

**Purpose**: User interface for customer interaction

**Components**:
- `App.jsx` - Main chat interface component
- `App.css` - Styling and animations
- `main.jsx` - Application entry point

**Features**:
- Real-time message display
- Session management
- Quick question shortcuts
- Typing indicators
- Escalation badges
- Responsive design

**Communication**:
- REST API calls via Axios
- WebSocket connection for real-time updates
- Proxy configuration in Vite for CORS handling

**Data Flow**:
```
User Input → React State → API Call → Backend → Response → UI Update
```

### 2. Backend Layer (FastAPI)

**Purpose**: API gateway and session management

**Components**:
- `main.py` - FastAPI application with endpoints
- `config.py` - Environment configuration
- Session storage (in-memory dictionary)

**Endpoints**:
```
POST   /query              - Process customer query
GET    /session/{id}       - Get session history
DELETE /session/{id}       - Clear session
WS     /ws/{id}           - WebSocket connection
GET    /                   - Health check
```

**Responsibilities**:
- HTTP request handling
- WebSocket management
- Session state persistence
- CORS configuration
- Request/response validation
- Error handling

### 3. Agent Orchestration Layer (LangGraph)

**Purpose**: Coordinate AI agents to process queries

#### Supervisor Agent

**Role**: Central coordinator

**Responsibilities**:
- Analyze incoming query
- Determine routing strategy
- Coordinate worker execution
- Ensure workflow completion

**Decision Logic**:
```python
if query_about_policies():
    route_to(knowledge_worker)
elif query_is_complaint():
    route_to(escalation_worker)
elif query_is_simple():
    route_to(response_worker)
else:
    route_to(knowledge_worker)  # Default
```

#### Knowledge Worker

**Role**: Information retrieval specialist

**Process**:
1. Receive query from supervisor
2. Generate query embedding
3. Search ChromaDB for similar documents
4. Retrieve top-k relevant chunks
5. Extract and summarize information
6. Return findings with confidence score

**Technology**:
- Vector similarity search
- HuggingFace embeddings (all-MiniLM-L6-v2)
- ChromaDB vector store
- GPT-4 for summarization

#### Response Worker

**Role**: Customer response generation

**Process**:
1. Receive query and knowledge from previous workers
2. Access conversation history
3. Generate contextual, friendly response
4. Apply brand voice and tone
5. Return final customer-facing message

**Guidelines**:
- Warm and professional tone
- Concise but complete
- Action-oriented when applicable
- Acknowledges limitations honestly

#### Escalation Worker

**Role**: Assess need for human intervention

**Process**:
1. Analyze query complexity and sentiment
2. Check against escalation criteria
3. Assign priority level
4. Generate handoff summary if needed
5. Return escalation decision

**Escalation Criteria**:
- High: Complaints, refunds, legal issues, security
- Medium: Complex technical issues, account problems
- Low: Standard questions handled by AI

### 4. Knowledge Base Layer

#### ChromaDB Vector Database

**Purpose**: Semantic search for knowledge retrieval

**Components**:
- Embeddings: Vector representations of text chunks
- Metadata: Source file, chunk index, etc.
- Similarity search: Cosine similarity for retrieval

**Initialization Process**:
```python
1. Load .txt files from knowledge/ folder
2. Split documents into chunks (1000 chars, 200 overlap)
3. Generate embeddings using HuggingFace model
4. Store in ChromaDB with metadata
5. Persist to disk (chroma_db/ folder)
```

**Query Process**:
```python
1. Receive query text
2. Generate query embedding
3. Search for k=3 most similar chunks
4. Return documents with similarity scores
```

#### Knowledge Documents

**Format**: Plain text files (.txt)

**Current Documents**:
- `return_policy.txt` - 350 lines
- `shipping_policy.txt` - 200 lines
- `faq.txt` - 450 lines
- `product_info.txt` - 300 lines
- `privacy_policy.txt` - 250 lines

**Adding New Knowledge**:
1. Create .txt file in knowledge/ folder
2. Restart backend server
3. Automatic reindexing occurs

## Data Flow

### Query Processing Flow

```
1. User enters query in React UI
   ↓
2. Frontend sends POST /query with:
   - query: string
   - session_id: string (optional)
   ↓
3. Backend receives request
   - Validates input
   - Retrieves session history
   - Formats chat context
   ↓
4. Calls LangGraph orchestrator
   - Initializes state graph
   ↓
5. Supervisor Agent analyzes query
   - Uses GPT-4 to understand intent
   - Decides which worker(s) to invoke
   ↓
6. Routes to appropriate worker(s):
   
   Path A: Knowledge Worker
   - Queries ChromaDB
   - Retrieves relevant docs
   - Summarizes with GPT-4
   ↓
   Path B: Escalation Worker
   - Analyzes sentiment/complexity
   - Determines if human needed
   - Generates handoff summary
   ↓
7. Response Worker
   - Receives query + knowledge/escalation info
   - Generates final response with GPT-4
   - Applies conversation context
   ↓
8. Backend receives final response
   - Updates session history
   - Prepares API response
   ↓
9. Frontend receives response
   - Updates chat UI
   - Displays message with styling
   - Shows escalation badge if needed
   ↓
10. User sees response
```

### Session Management

```
Session Structure:
{
  "session_id": "session_1234567890_abc123",
  "messages": [
    {
      "role": "user" | "assistant",
      "content": "message text",
      "timestamp": "2025-01-01T12:00:00"
    },
    ...
  ]
}

Lifecycle:
1. Create on first query (if no session_id provided)
2. Maintain in memory during conversation
3. Last 5 messages included in context
4. Cleared on user request or server restart
```

## Agent State Graph (LangGraph)

```
State Schema:
{
  messages: List[BaseMessage]      # LangChain messages
  query: str                       # Current user query
  chat_history: str                # Formatted history
  next_worker: str                 # Routing decision
  knowledge_retrieved: str         # Knowledge findings
  escalation_needed: bool          # Escalation flag
  final_response: str              # Customer response
}

Graph Flow:
┌──────────────┐
│   START      │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  Supervisor  │──────┐
└──────┬───────┘      │
       │              │ Decision: FINISH
       │              │
       ↓              ↓
  [Route Based     ┌─────┐
   on Decision]    │ END │
       │           └─────┘
   ┌───┴───┬────────────┐
   │       │            │
   ↓       ↓            ↓
┌────┐  ┌────┐    ┌──────────┐
│Know│  │Esc │    │Response  │
│ledge│ │alat│    │Worker    │
│Work│  │ion │    └────┬─────┘
│er  │  │Work│         │
└─┬──┘  │er  │         │
  │     └─┬──┘         │
  │       │            │
  └───────┴────────────┘
          │
          ↓
    ┌──────────┐
    │Response  │
    │Worker    │
    └────┬─────┘
         │
         ↓
      ┌─────┐
      │ END │
      └─────┘
```

## Technology Stack Details

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Runtime environment |
| FastAPI | 0.109.0 | Web framework |
| Uvicorn | 0.27.0 | ASGI server |
| LangChain | 0.1.4 | LLM framework |
| LangGraph | 0.0.20 | Agent orchestration |
| ChromaDB | 0.4.22 | Vector database |
| Sentence Transformers | 2.3.1 | Embeddings |
| OpenAI SDK | Latest | GPT-4 API |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI library |
| Vite | 5.0.11 | Build tool |
| Axios | 1.6.5 | HTTP client |
| CSS3 | - | Styling |

### AI/ML Technologies

| Component | Model/Technology |
|-----------|-----------------|
| LLM | GPT-4-turbo-preview |
| Embeddings | all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| Framework | LangGraph |

## Deployment Architecture

### Development

```
Local Machine
├── Backend (localhost:8000)
│   └── Python venv
├── Frontend (localhost:3000)
│   └── Vite dev server
└── ChromaDB (./backend/chroma_db/)
```

### Docker Deployment

```
Docker Compose
├── backend container
│   ├── Python app
│   ├── ChromaDB volume
│   └── Port 8000
├── frontend container
│   ├── Nginx server
│   ├── Built React app
│   └── Port 3000
└── Network: app-network
```

## Security Considerations

1. **API Keys**: Stored in .env, never committed
2. **CORS**: Configured for specific origins
3. **Input Validation**: Pydantic models
4. **Session Security**: In-memory storage (upgrade to Redis for production)
5. **Rate Limiting**: Should be added for production
6. **HTTPS**: Should be enforced in production

## Performance Considerations

1. **First Query Delay**: Knowledge base initialization (~2-5s)
2. **Subsequent Queries**: Faster (~1-3s depending on LLM)
3. **Caching**: ChromaDB caches embeddings
4. **Session Storage**: In-memory for speed (limited scalability)
5. **Concurrent Requests**: FastAPI handles async requests

## Scalability

### Current Limitations
- In-memory session storage (single instance)
- Local ChromaDB (not distributed)
- Single FastAPI instance

### Production Improvements
- Redis for session storage
- Distributed vector database (Pinecone, Weaviate)
- Load balancer for multiple backend instances
- CDN for frontend assets
- Kubernetes deployment

## Monitoring & Observability

### Recommended Additions
- Prometheus metrics
- Grafana dashboards
- LangSmith tracing
- Error tracking (Sentry)
- Performance monitoring (New Relic)

## Future Enhancements

1. **Multi-tenancy**: Support multiple organizations
2. **Custom Models**: Fine-tuned models for specific domains
3. **Analytics Dashboard**: Query insights and metrics
4. **A/B Testing**: Experiment with different prompts
5. **Feedback Loop**: Learn from user ratings
6. **Multi-language**: Support for international customers
7. **Voice Interface**: Speech-to-text integration
8. **Mobile App**: Native iOS/Android apps

