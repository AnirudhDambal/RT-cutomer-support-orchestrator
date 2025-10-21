import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:8888'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Generate session ID on mount
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    setSessionId(newSessionId)
    
    // Add welcome message
    setMessages([{
      role: 'assistant',
      content: 'Hello! I\'m your AI customer support assistant. How can I help you today?',
      timestamp: new Date().toISOString()
    }])
  }, [])

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim() || loading) return

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        query: userMessage.content,
        session_id: sessionId
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: response.data.timestamp,
        escalation_needed: response.data.escalation_needed
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      const errorMessage = {
        role: 'assistant',
        content: 'I apologize, but I\'m having trouble processing your request right now. Please try again or contact our support team directly.',
        timestamp: new Date().toISOString(),
        error: true
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearChat = async () => {
    if (sessionId) {
      try {
        await axios.delete(`${API_BASE_URL}/session/${sessionId}`)
      } catch (error) {
        console.error('Error clearing session:', error)
      }
    }
    
    // Generate new session ID
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    setSessionId(newSessionId)
    
    // Reset messages with welcome message
    setMessages([{
      role: 'assistant',
      content: 'Hello! I\'m your AI customer support assistant. How can I help you today?',
      timestamp: new Date().toISOString()
    }])
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className="app-container">
      <div className="chat-container">
        {/* Header */}
        <div className="chat-header">
          <div className="header-content">
            <div className="header-title">
              <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <h1>AI Customer Support</h1>
            </div>
            <button onClick={clearChat} className="clear-button" title="New Conversation">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                <div className="message-bubble">
                  {message.content}
                  {message.escalation_needed && (
                    <div className="escalation-badge">
                      ⚠️ Escalated to human support
                    </div>
                  )}
                  {message.error && (
                    <div className="error-badge">
                      ❌ Error occurred
                    </div>
                  )}
                </div>
                <div className="message-time">
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="message-bubble typing">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="input-container">
          <form onSubmit={sendMessage} className="input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="message-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={loading || !input.trim()}
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      </div>

      {/* Info Panel */}
      <div className="info-panel">
        <h2>Quick Help</h2>
        <div className="info-section">
          <h3>Common Questions</h3>
          <button 
            className="quick-question"
            onClick={() => setInput("What is your return policy?")}
          >
            What is your return policy?
          </button>
          <button 
            className="quick-question"
            onClick={() => setInput("How can I track my order?")}
          >
            How can I track my order?
          </button>
          <button 
            className="quick-question"
            onClick={() => setInput("What shipping options do you offer?")}
          >
            What shipping options do you offer?
          </button>
          <button 
            className="quick-question"
            onClick={() => setInput("Tell me about the Premium Wireless Headphones")}
          >
            Product information
          </button>
        </div>
        
        <div className="info-section">
          <h3>Features</h3>
          <ul className="feature-list">
            <li>✨ AI-powered responses</li>
            <li>📚 Knowledge base retrieval</li>
            <li>🔄 Context-aware conversations</li>
            <li>🚀 Instant support 24/7</li>
            <li>👤 Human escalation when needed</li>
          </ul>
        </div>

        <div className="info-section">
          <h3>Need Human Help?</h3>
          <p className="contact-info">
            📧 support@company.com<br />
            📞 1-800-SUPPORT<br />
            🕐 Mon-Fri 9AM-8PM EST
          </p>
        </div>
      </div>
    </div>
  )
}

export default App

