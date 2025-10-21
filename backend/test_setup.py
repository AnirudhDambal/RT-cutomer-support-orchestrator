#!/usr/bin/env python3
"""
Test Setup Script - Verify environment and API connectivity before starting backend
"""
import sys
import os
from pathlib import Path

def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "success": "\033[92m✓",
        "error": "\033[91m✗",
        "warning": "\033[93m⚠",
        "info": "\033[94mℹ"
    }
    reset = "\033[0m"
    symbol = colors.get(status, colors["info"])
    print(f"{symbol} {message}{reset}")

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("1. Testing Package Imports")
    print("="*60)
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("langchain", "LangChain"),
        ("langgraph", "LangGraph"),
        ("langchain_openai", "LangChain OpenAI"),
        ("langchain_community", "LangChain Community"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
        ("dotenv", "Python Dotenv"),
    ]
    
    all_good = True
    for package, name in packages:
        try:
            __import__(package)
            print_status(f"{name} installed", "success")
        except ImportError as e:
            print_status(f"{name} NOT installed - {e}", "error")
            all_good = False
    
    return all_good

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n" + "="*60)
    print("2. Testing Environment Configuration")
    print("="*60)
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print_status(".env file NOT found", "error")
        print_status("Create it with: echo 'OPENAI_API_KEY=your_key' > .env", "warning")
        return False
    
    print_status(".env file exists", "success")
    
    # Try to load it
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Check for placeholder keys
    placeholder_keys = [
        "your_google_api_key_here",
        "your_api_key_here",
        "your_key_here",
        "your_actual_key_here",
        "your_key",
    ]
    
    if not api_key:
        print_status("GOOGLE_API_KEY not found in .env", "error")
        print_status("Get your key from: https://makersuite.google.com/app/apikey", "warning")
        return False
    
    if api_key in placeholder_keys or "your" in api_key.lower():
        print_status(f"Placeholder API key detected: {api_key}", "error")
        print_status("Replace with your REAL Google API key", "warning")
        print_status("Get your key from: https://makersuite.google.com/app/apikey", "warning")
        return False
    
    if not api_key.startswith("AIza"):
        print_status("Invalid API key format (should start with 'AIza')", "error")
        return False
    
    if len(api_key) < 20:
        print_status("GOOGLE_API_KEY too short (invalid)", "error")
        return False
    
    # Mask the key for security
    masked_key = api_key[:10] + "..." + api_key[-4:]
    print_status(f"GOOGLE_API_KEY found: {masked_key}", "success")
    
    return True

def test_gemini_connection():
    """Test Google Gemini API connection"""
    print("\n" + "="*60)
    print("3. Testing Google Gemini API Connection")
    print("="*60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        print_status("Creating Gemini client...", "info")
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0,
            max_output_tokens=10
        )
        
        print_status("Sending test request...", "info")
        response = llm.invoke("Say 'OK' if you can read this")
        
        print_status(f"API Response: {response.content}", "success")
        print_status("Google Gemini API connection successful!", "success")
        return True
        
    except Exception as e:
        print_status(f"Gemini API connection failed: {e}", "error")
        print_status("Check your API key and internet connection", "warning")
        return False

def test_knowledge_base():
    """Test knowledge base folder"""
    print("\n" + "="*60)
    print("4. Testing Knowledge Base")
    print("="*60)
    
    knowledge_path = Path("../knowledge")
    
    if not knowledge_path.exists():
        print_status(f"Knowledge folder not found at {knowledge_path}", "error")
        return False
    
    print_status(f"Knowledge folder found: {knowledge_path.absolute()}", "success")
    
    txt_files = list(knowledge_path.glob("*.txt"))
    
    if not txt_files:
        print_status("No .txt files found in knowledge folder", "warning")
        return False
    
    print_status(f"Found {len(txt_files)} knowledge documents:", "success")
    for txt_file in txt_files:
        file_size = txt_file.stat().st_size
        print_status(f"  - {txt_file.name} ({file_size} bytes)", "info")
    
    return True

def test_vector_db():
    """Test vector database initialization"""
    print("\n" + "="*60)
    print("5. Testing Vector Database")
    print("="*60)
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        print_status("Loading embedding model (this may take a moment)...", "info")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        print_status("Embedding model loaded successfully", "success")
        
        # Test embedding
        test_text = "This is a test"
        print_status("Generating test embedding...", "info")
        test_embedding = embeddings.embed_query(test_text)
        
        print_status(f"Embedding generated (dimension: {len(test_embedding)})", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Vector database test failed: {e}", "error")
        return False

def test_document_loading():
    """Test loading documents from knowledge base"""
    print("\n" + "="*60)
    print("6. Testing Document Loading")
    print("="*60)
    
    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        knowledge_path = Path("../knowledge")
        
        print_status("Loading documents...", "info")
        loader = DirectoryLoader(
            str(knowledge_path),
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        
        documents = loader.load()
        
        if not documents:
            print_status("No documents loaded", "warning")
            return False
        
        print_status(f"Loaded {len(documents)} documents", "success")
        
        print_status("Splitting documents into chunks...", "info")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        print_status(f"Created {len(splits)} chunks", "success")
        
        # Show sample
        if splits:
            sample = splits[0].page_content[:100]
            print_status(f"Sample chunk: {sample}...", "info")
        
        return True
        
    except Exception as e:
        print_status(f"Document loading failed: {e}", "error")
        return False

def test_config():
    """Test config.py loading"""
    print("\n" + "="*60)
    print("7. Testing Configuration Module")
    print("="*60)
    
    try:
        from config import settings
        
        print_status("Configuration loaded successfully", "success")
        print_status(f"Knowledge Path: {settings.knowledge_path}", "info")
        print_status(f"ChromaDB Path: {settings.chroma_db_path}", "info")
        
        # Check if API key is loaded
        if settings.google_api_key:
            masked_key = settings.google_api_key[:10] + "..." + settings.google_api_key[-4:]
            print_status(f"API Key: {masked_key}", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Config loading failed: {e}", "error")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "BACKEND SETUP TEST SUITE" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {}
    
    results['imports'] = test_imports()
    results['env'] = test_env_file()
    
    if results['env']:
        results['gemini'] = test_gemini_connection()
    else:
        print_status("\nSkipping Gemini test (no valid .env file)", "warning")
        results['gemini'] = False
    
    results['knowledge'] = test_knowledge_base()
    results['vector_db'] = test_vector_db()
    results['documents'] = test_document_loading()
    results['config'] = test_config()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(results.values())
    
    for test_name, passed_test in results.items():
        status = "success" if passed_test else "error"
        print_status(f"{test_name.upper()}: {'PASS' if passed_test else 'FAIL'}", status)
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print_status("\n🎉 ALL TESTS PASSED! You're ready to start the backend!", "success")
        print("\nRun the backend with:")
        print("  python main.py")
        return True
    else:
        print_status("\n❌ Some tests failed. Please fix the issues above.", "error")
        
        if not results['env']:
            print("\n📝 Quick Fix:")
            print("  echo 'OPENAI_API_KEY=your_actual_key_here' > .env")
        
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\n\nTest interrupted by user", "warning")
        sys.exit(1)
    except Exception as e:
        print_status(f"\n\nUnexpected error: {e}", "error")
        import traceback
        traceback.print_exc()
        sys.exit(1)

