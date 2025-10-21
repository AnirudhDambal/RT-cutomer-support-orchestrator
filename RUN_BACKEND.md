# 🚀 Start the Backend

## ✅ Port 8888 is Ready and All Errors Are Fixed!

---

## Run This Command:

```bash
cd /Users/vadirajdeshpande/RT-cutomer-support-orchestrator/backend
./venv/bin/python main.py
```

**You should see:**
```
Loaded 5 documents with 17 chunks into vector store
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8888
```

**Keep this terminal open!** The backend will run here.

---

## Then Test It (in a NEW terminal):

```bash
# Test root endpoint
curl http://localhost:8888/

# Test query endpoint
curl -X POST http://localhost:8888/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'

# Or use the interactive API docs
open http://localhost:8888/docs
```

---

## Start Frontend (in another terminal):

```bash
cd /Users/vadirajdeshpande/RT-cutomer-support-orchestrator/frontend
npm run dev
```

Then open: **http://localhost:3000**

---

## Summary:

✅ **Fixed:** Syntax error in `agents.py` (API key now uses settings)  
✅ **Fixed:** Port 8888 is free and configured  
✅ **Ready:** Backend is ready to start  
✅ **Ready:** Frontend configured for port 8888  

**Just run the python command above and you're good to go!** 🎉

