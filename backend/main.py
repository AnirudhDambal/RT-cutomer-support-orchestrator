"""
FastAPI Backend for Customer Support Orchestrator
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

from agents import CustomerSupportOrchestrator
from config import settings

app = FastAPI(
    title="Customer Support Orchestrator",
    description="AI-powered customer support with LangGraph agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = CustomerSupportOrchestrator()

# Store chat sessions in memory (in production, use Redis or database)
chat_sessions = {}


class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    escalation_needed: bool
    knowledge_used: str
    session_id: str
    timestamp: str


@app.get("/")
async def root():
    return {
        "message": "Customer Support Orchestrator API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a customer support query"""
    try:
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Get chat history for this session
        chat_history = chat_sessions.get(session_id, [])
        chat_history_str = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in chat_history[-5:]  # Last 5 messages
        ])
        
        # Process query
        result = orchestrator.process_query(
            query=request.query,
            chat_history=chat_history_str
        )
        
        # Update chat history
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_sessions[session_id].append({
            "role": "user",
            "content": request.query,
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            response=result["response"],
            escalation_needed=result["escalation_needed"],
            knowledge_used=result["knowledge_used"],
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}")
async def get_session_history(session_id: str):
    """Get chat history for a session"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "messages": chat_sessions[session_id]
    }


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    
    raise HTTPException(status_code=404, detail="Session not found")


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            query_data = json.loads(data)
            query = query_data.get("query", "")
            
            if not query:
                await websocket.send_json({"error": "Empty query"})
                continue
            
            # Get chat history
            chat_history = chat_sessions.get(session_id, [])
            chat_history_str = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in chat_history[-5:]
            ])
            
            # Process query
            result = orchestrator.process_query(
                query=query,
                chat_history=chat_history_str
            )
            
            # Update session
            if session_id not in chat_sessions:
                chat_sessions[session_id] = []
            
            chat_sessions[session_id].append({
                "role": "user",
                "content": query,
                "timestamp": datetime.now().isoformat()
            })
            chat_sessions[session_id].append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            
            # Send response
            await websocket.send_json({
                "response": result["response"],
                "escalation_needed": result["escalation_needed"],
                "timestamp": datetime.now().isoformat()
            })
    
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)

