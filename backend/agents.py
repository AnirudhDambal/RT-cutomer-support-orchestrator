"""
LangGraph Agent System with Supervisor and Workers
"""
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import operator
from pathlib import Path
import os

from prompts import (
    SUPERVISOR_PROMPT,
    KNOWLEDGE_WORKER_PROMPT,
    RESPONSE_WORKER_PROMPT,
    ESCALATION_WORKER_PROMPT
)
from config import settings

# State definition for the agent graph
class AgentState(TypedDict):
    """State shared across all agents"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    chat_history: str
    next_worker: str
    knowledge_retrieved: str
    escalation_needed: bool
    final_response: str


class CustomerSupportOrchestrator:
    """Main orchestrator using LangGraph with Supervisor-Worker pattern"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=settings.google_api_key
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.graph = None
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
        
        # Build the agent graph
        self._build_graph()
    
    def _initialize_knowledge_base(self):
        """Load documents from knowledge folder and create vector store"""
        knowledge_path = Path(settings.knowledge_path)
        
        if not knowledge_path.exists():
            print(f"Warning: Knowledge path {knowledge_path} does not exist")
            return
        
        # Load all text files from knowledge folder
        loader = DirectoryLoader(
            str(knowledge_path),
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        
        try:
            documents = loader.load()
            
            if not documents:
                print("Warning: No documents found in knowledge folder")
                return
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=settings.chroma_db_path
            )
            print(f"Loaded {len(documents)} documents with {len(splits)} chunks into vector store")
            
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    
    def supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor decides which worker to route to next"""
        query = state["query"]
        chat_history = state.get("chat_history", "")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", SUPERVISOR_PROMPT),
            ("human", "Decide the next worker: knowledge_worker, response_worker, escalation_worker, or FINISH")
        ])
        
        formatted_prompt = SUPERVISOR_PROMPT.format(
            query=query,
            chat_history=chat_history
        )
        
        response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
        decision = response.content.lower()
        
        # Parse decision
        if "knowledge_worker" in decision:
            next_worker = "knowledge_worker"    
        elif "escalation_worker" in decision:
            next_worker = "escalation_worker"
        elif "response_worker" in decision:
            next_worker = "response_worker"
        else:
            next_worker = "FINISH"
        
        state["next_worker"] = next_worker
        state["messages"] = state.get("messages", []) + [response]
        
        return state
    
    def knowledge_worker_node(self, state: AgentState) -> AgentState:
        """Knowledge worker retrieves relevant information from vector store"""
        query = state["query"]
        
        # Retrieve relevant documents
        context = ""
        if self.vector_store:
            docs = self.vector_store.similarity_search(query, k=3)
            context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
        else:
            context = "No knowledge base available"
        
        # Process with LLM
        prompt = KNOWLEDGE_WORKER_PROMPT.format(query=query, context=context)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        state["knowledge_retrieved"] = response.content
        state["messages"] = state.get("messages", []) + [response]
        state["next_worker"] = "response_worker"  # Always go to response worker after retrieval
        
        return state
    
    def response_worker_node(self, state: AgentState) -> AgentState:
        """Response worker generates the final customer-facing response"""
        query = state["query"]
        knowledge = state.get("knowledge_retrieved", "No specific knowledge retrieved")
        chat_history = state.get("chat_history", "")
        
        prompt = RESPONSE_WORKER_PROMPT.format(
            query=query,
            knowledge=knowledge,
            chat_history=chat_history
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        state["final_response"] = response.content
        state["messages"] = state.get("messages", []) + [response]
        state["next_worker"] = "FINISH"
        
        return state
    
    def escalation_worker_node(self, state: AgentState) -> AgentState:
        """Escalation worker assesses if human intervention is needed"""
        query = state["query"]
        context = state.get("knowledge_retrieved", "")
        chat_history = state.get("chat_history", "")
        
        prompt = ESCALATION_WORKER_PROMPT.format(
            query=query,
            context=context,
            chat_history=chat_history
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        # Check if escalation is needed
        escalation_needed = "escalation needed: yes" in response.content.lower()
        
        state["escalation_needed"] = escalation_needed
        state["messages"] = state.get("messages", []) + [response]
        
        if escalation_needed:
            state["final_response"] = (
                "This query requires human assistance. A support agent will contact you shortly.\n\n"
                f"Assessment: {response.content}"
            )
            state["next_worker"] = "FINISH"
        else:
            state["next_worker"] = "response_worker"
        
        return state
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("supervisor", self.supervisor_node)
        workflow.add_node("knowledge_worker", self.knowledge_worker_node)
        workflow.add_node("response_worker", self.response_worker_node)
        workflow.add_node("escalation_worker", self.escalation_worker_node)
        
        # Add edges
        workflow.set_entry_point("supervisor")
        
        # Conditional routing from supervisor
        def route_supervisor(state: AgentState) -> str:
            next_worker = state.get("next_worker", "FINISH")
            if next_worker == "FINISH":
                return END
            return next_worker
        
        workflow.add_conditional_edges(
            "supervisor",
            route_supervisor,
            {
                "knowledge_worker": "knowledge_worker",
                "response_worker": "response_worker",
                "escalation_worker": "escalation_worker",
                END: END
            }
        )
        
        # Workers route back to supervisor or to next worker
        workflow.add_edge("knowledge_worker", "response_worker")
        workflow.add_edge("response_worker", END)
        
        def route_escalation(state: AgentState) -> str:
            if state.get("next_worker") == "FINISH":
                return END
            return "response_worker"
        
        workflow.add_conditional_edges(
            "escalation_worker",
            route_escalation,
            {
                "response_worker": "response_worker",
                END: END
            }
        )
        
        # Compile the graph
        self.graph = workflow.compile()
    
    def process_query(self, query: str, chat_history: str = "") -> dict:
        """Process a customer query through the agent system"""
        initial_state = {
            "messages": [],
            "query": query,
            "chat_history": chat_history,
            "next_worker": "",
            "knowledge_retrieved": "",
            "escalation_needed": False,
            "final_response": ""
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        return {
            "response": final_state.get("final_response", "I apologize, I couldn't process your query."),
            "escalation_needed": final_state.get("escalation_needed", False),
            "knowledge_used": final_state.get("knowledge_retrieved", "")
        }

