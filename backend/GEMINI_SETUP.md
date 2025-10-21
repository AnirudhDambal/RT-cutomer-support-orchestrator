# 🚀 Quick Setup with Google Gemini

## 3-Step Setup

### 1️⃣ Get API Key (FREE!)
Go to: **https://makersuite.google.com/app/apikey**
- Click "Get API key"
- Copy the key (starts with `AIza...`)

### 2️⃣ Configure
```bash
cd backend
python setup_env.py
# Paste your API key when prompted
```

### 3️⃣ Run
```bash
python quick_test.py  # Verify setup
python main.py        # Start backend
```

---

## Why Gemini?

✅ **FREE** - No credit card required  
✅ **Fast** - Low latency responses  
✅ **Quality** - Competitive with GPT-4  
✅ **Generous** - 60 requests/min free  

---

## API Key Format

**Google Gemini:**
```
GOOGLE_API_KEY=AIzaSyABC123...
```

**Starts with:** `AIza`  
**Length:** ~39 characters  
**Cost:** FREE (with limits)

---

## Quick Commands

```bash
# Setup
cd /Users/vadirajdeshpande/RT-cutomer-support-orchestrator/backend
source venv/bin/activate
pip install -r requirements.txt

# Configure (interactive)
python setup_env.py

# Test
python quick_test.py

# Run
python main.py
```

---

## Troubleshooting

**"Invalid API key"**
- Check it starts with `AIza`
- No extra spaces or quotes
- Get new key if expired

**"Quota exceeded"**
- Free tier: 60 req/min
- Wait 1 minute or upgrade

**"Import error"**
```bash
pip install langchain-google-genai google-generativeai
```

---

## Resources

- API Keys: https://makersuite.google.com/app/apikey
- Documentation: https://ai.google.dev/docs
- Pricing: https://ai.google.dev/pricing (FREE tier available!)

---

**Ready in 3 minutes!** 🎉

