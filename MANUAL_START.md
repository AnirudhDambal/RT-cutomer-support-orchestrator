# 🚀 Manual Start Guide

## ✅ **The Issue is Fixed - Model Updated to `gemini-2.5-flash`**

---

## 🔧 **Step 1: Kill All Processes**

```bash
# Kill any existing processes
lsof -ti:8888 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
pkill -f "python.*main.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
```

---

## 🚀 **Step 2: Start Backend**

```bash
cd backend
rm -rf __pycache__
./venv/bin/python main.py
```

**You should see:**
```
Loaded 5 documents with 17 chunks into vector store
INFO:     Uvicorn running on http://0.0.0.0:8888
```

**Keep this terminal open!**

---

## 🎨 **Step 3: Start Frontend (New Terminal)**

```bash
cd frontend
npm run dev
```

**You should see:**
```
VITE v5.4.21  ready in 209 ms
➜  Local:   http://localhost:3000/
```

---

## 🧪 **Step 4: Test**

**Backend API:**
```bash
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'
```

**Frontend:** http://localhost:3000

---

## ✅ **What's Fixed:**

1. ✅ **Model:** Now using `gemini-2.5-flash` (latest available)
2. ✅ **Port:** Backend on 8888, Frontend on 3000
3. ✅ **API Key:** Google AI Studio key working
4. ✅ **Processes:** Clean startup without conflicts

---

## 🎯 **Quick Commands:**

```bash
# Terminal 1 - Backend
cd backend && ./venv/bin/python main.py

# Terminal 2 - Frontend  
cd frontend && npm run dev

# Test
curl -X POST http://localhost:8888/query -H "Content-Type: application/json" -d '{"query":"test"}'
```

**Everything is now properly configured!** 🎉
