# 🚀 How to Start and Test the Backend

## ✅ Quick Start

### 1️⃣ Start the Backend
```bash
cd /Users/vadirajdeshpande/RT-cutomer-support-orchestrator/backend
source venv/bin/activate
python main.py
```

You should see:
```
Loaded 5 documents with X chunks into vector store
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2️⃣ Test the API (in a new terminal)

**Option A: Use the test script**
```bash
cd backend
python test_api.py
```

**Option B: Use curl**
```bash
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is your return policy?"}'
```

**Option C: Use the API docs**
Open your browser: **http://localhost:8000/docs**
- Click on `/query`
- Click "Try it out"
- Enter a query
- Click "Execute"

---

## 📝 Important Notes

### ❌ **Why `/query` Doesn't Work in Browser**

When you type `http://localhost:8000/query` in your browser:
- Browser sends a **GET** request
- The `/query` endpoint requires a **POST** request with JSON data
- That's why you get "Not Found"!

### ✅ **Correct Ways to Test**

1. **Interactive API Docs** (Easiest!)
   - Go to: `http://localhost:8000/docs`
   - Click on POST `/query`
   - Test it visually!

2. **curl Command** (Terminal)
   ```bash
   curl -X POST http://localhost:8000/query \
     -H 'Content-Type: application/json' \
     -d '{"query": "Your question here"}'
   ```

3. **Python Script** (test_api.py)
   ```bash
   python test_api.py
   ```

4. **Frontend** (React app)
   ```bash
   cd ../frontend
   npm run dev
   # Open http://localhost:3000
   ```

---

## 📋 Available Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/query` | Send a question |
| GET | `/session/{id}` | Get chat history |
| DELETE | `/session/{id}` | Clear session |
| WebSocket | `/ws/{id}` | Real-time chat |
| GET | `/docs` | API documentation |

---

## 🧪 Test Queries

Try these questions:
- "What is your return policy?"
- "How long does shipping take?"
- "Tell me about the Premium Wireless Headphones"
- "I want to return a defective product"
- "What payment methods do you accept?"

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check for errors
python main.py

# Common issues:
# 1. Port 8000 already in use
# 2. Missing dependencies
# 3. Invalid API key
```

### "Connection refused"?
- Backend not running
- Start it with: `python main.py`

### "Not Found" error?
- You're using GET instead of POST
- Use the API docs or curl command above

### "Invalid API key"?
```bash
# Check your .env file
cat .env

# Should show:
# GOOGLE_API_KEY=AIzaSy...
```

---

## 💡 Quick Reference

```bash
# Start backend
cd backend && source venv/bin/activate && python main.py

# Test in new terminal
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"query": "test"}'

# Or use API docs
open http://localhost:8000/docs
```

---

**📌 Remember:** The `/query` endpoint is **POST only**, not GET!  
**Use the API docs at http://localhost:8000/docs for easy testing!** 🎉

