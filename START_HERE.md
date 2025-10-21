# 🚀 Quick Start Guide

## ✅ Backend and Frontend are Now Configured for Port 8888

---

## 🎯 Start the Backend

### Option 1: Using the Start Script (Easy!)
```bash
cd backend
./start.sh
```

### Option 2: Manual Start
```bash
cd backend
./venv/bin/python main.py
```

**You should see:**
```
Loaded 5 documents with 17 chunks into vector store
INFO:     Uvicorn running on http://0.0.0.0:8888
```

**Keep this terminal open!**

---

## 🎨 Start the Frontend

Open a **NEW terminal** and run:

```bash
cd frontend
npm install  # Only needed first time
npm run dev
```

**You should see:**
```
  VITE v5.0.11  ready in 500 ms
  ➜  Local:   http://localhost:3000/
```

---

## 🧪 Test the Backend (Optional)

In another terminal:

```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'
```

Or visit the API docs:
```
http://localhost:8888/docs
```

---

## 🌐 Access the Application

Once both are running:

- **Frontend (Chat UI):** http://localhost:3000
- **Backend API:** http://localhost:8888
- **API Documentation:** http://localhost:8888/docs

---

## 🐛 Troubleshooting

### Backend won't start?

**Check port 8888 is free:**
```bash
lsof -i :8888
```

**Kill any process on port 8888:**
```bash
kill -9 $(lsof -ti:8888)
```

### "Module not found" error?

```bash
cd backend
./venv/bin/pip install -r requirements.txt
```

### Frontend can't connect?

- Make sure backend is running on port 8888
- Check browser console for errors (F12)

---

## 📝 Summary

**Ports Configured:**
- Backend: **8888**
- Frontend: **3000**

**Commands:**
```bash
# Terminal 1 - Backend
cd backend && ./start.sh

# Terminal 2 - Frontend
cd frontend && npm run dev

# Open browser: http://localhost:3000
```

---

**That's it! Your AI Customer Support system is ready to use! 🎉**

