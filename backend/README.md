# Backend - Customer Support Orchestrator

This is the backend service powered by LangGraph with a supervisor-worker agent architecture.

## Architecture

### Agent System (LangGraph)

The system uses a **Supervisor-Worker** pattern with the following agents:

1. **Supervisor Agent**
   - Coordinates all worker agents
   - Routes queries to appropriate workers
   - Makes decisions on workflow execution

2. **Knowledge Worker**
   - Retrieves relevant information from the knowledge base
   - Uses vector similarity search (ChromaDB)
   - Extracts and summarizes relevant policy documents

3. **Response Worker**
   - Generates customer-friendly responses
   - Uses knowledge retrieved by the Knowledge Worker
   - Maintains context and conversation history

4. **Escalation Worker**
   - Assesses if human intervention is needed
   - Categorizes urgency levels
   - Provides handoff summaries for human agents

### Knowledge Base

Located in the `../knowledge` folder:
- `return_policy.txt` - Return and refund policies
- `shipping_policy.txt` - Shipping and delivery information
- `faq.txt` - Frequently asked questions
- `product_info.txt` - Product details and troubleshooting
- `privacy_policy.txt` - Privacy and data protection information

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
KNOWLEDGE_PATH=../knowledge
CHROMA_DB_PATH=./chroma_db
```

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /query
Process a customer support query

**Request:**
```json
{
  "query": "What is your return policy?",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "Our return policy allows...",
  "escalation_needed": false,
  "knowledge_used": "Retrieved from return_policy.txt...",
  "session_id": "session_12345",
  "timestamp": "2025-01-01T12:00:00"
}
```

### GET /session/{session_id}
Get chat history for a session

### DELETE /session/{session_id}
Clear a chat session

### WebSocket /ws/{session_id}
Real-time chat via WebSocket

## Agent Flow

```
User Query → Supervisor Agent
              ↓
    Decision: Route to Worker
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Knowledge Worker    Escalation Worker
    ↓                   ↓
Response Worker ← ──────┘
    ↓
Final Response to User
```

## Customization

### Modify Agent Prompts

Edit `prompts.py` to customize agent behavior:
- `SUPERVISOR_PROMPT` - Supervisor decision-making
- `KNOWLEDGE_WORKER_PROMPT` - Knowledge retrieval behavior
- `RESPONSE_WORKER_PROMPT` - Response generation style
- `ESCALATION_WORKER_PROMPT` - Escalation criteria

### Add More Knowledge

Add `.txt` files to the `knowledge/` folder. The system will automatically:
1. Load the documents
2. Split into chunks
3. Generate embeddings
4. Store in ChromaDB vector database

### Change LLM Model

In `agents.py`, modify the ChatOpenAI initialization:

```python
self.llm = ChatOpenAI(
    model="gpt-4-turbo-preview",  # Change model here
    temperature=0.7,
    openai_api_key=settings.openai_api_key
)
```

## Troubleshooting

**Issue: "No knowledge base available"**
- Ensure the `knowledge/` folder exists and contains `.txt` files
- Check the `KNOWLEDGE_PATH` in `.env`

**Issue: ChromaDB errors**
- Delete the `chroma_db/` folder and restart the server
- This will rebuild the vector database

**Issue: OpenAI API errors**
- Verify your API key is valid
- Check you have sufficient credits
- Ensure the model name is correct

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

```
backend/
├── main.py          # FastAPI application
├── agents.py        # LangGraph agent system
├── prompts.py       # Agent prompts
├── config.py        # Configuration settings
└── requirements.txt # Dependencies
```

