#!/usr/bin/env python3
"""
Interactive .env Setup Script
Helps users configure their environment file
"""
import os
from pathlib import Path

def print_banner():
    print("\n" + "="*60)
    print("   🔑 Google Gemini API Key Setup")
    print("="*60 + "\n")

def get_api_key():
    """Interactively get API key from user"""
    print("📝 You need a Google API key to use this application.\n")
    print("Get your API key from:")
    print("   👉 https://makersuite.google.com/app/apikey\n")
    
    print("Steps:")
    print("   1. Sign in to your Google account")
    print("   2. Click 'Get API key' or 'Create API key'")
    print("   3. Copy the key (starts with 'AIza')")
    print("   4. Paste it below\n")
    
    while True:
        api_key = input("Enter your Google API key: ").strip()
        
        if not api_key:
            print("❌ API key cannot be empty. Please try again.\n")
            continue
        
        if not api_key.startswith("AIza"):
            print("❌ Invalid format. Google API keys start with 'AIza'")
            retry = input("   Try again? (y/n): ").lower()
            if retry != 'y':
                return None
            continue
        
        if len(api_key) < 20:
            print("❌ Key seems too short. Please check and try again.")
            retry = input("   Try again? (y/n): ").lower()
            if retry != 'y':
                return None
            continue
        
        # Confirm
        masked = api_key[:10] + "..." + api_key[-4:]
        print(f"\n✓ Key received: {masked}")
        confirm = input("  Is this correct? (y/n): ").lower()
        
        if confirm == 'y':
            return api_key
        else:
            print("  Let's try again.\n")

def create_env_file(api_key):
    """Create .env file with API key"""
    env_content = f"""# Google Gemini API Configuration
GOOGLE_API_KEY={api_key}

# Optional: Customize these if needed
# KNOWLEDGE_PATH=../knowledge
# CHROMA_DB_PATH=./chroma_db
"""
    
    env_path = Path(".env")
    
    # Check if .env already exists
    if env_path.exists():
        print("\n⚠️  .env file already exists!")
        overwrite = input("   Overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("   Cancelled. Existing .env file preserved.")
            return False
    
    # Write the file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created successfully!")
    print(f"   Location: {env_path.absolute()}")
    
    return True

def verify_setup():
    """Verify the setup by loading .env"""
    print("\n" + "="*60)
    print("   🔍 Verifying Setup")
    print("="*60 + "\n")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if api_key and api_key.startswith("AIza") and len(api_key) > 20:
            masked = api_key[:10] + "..." + api_key[-4:]
            print(f"✓ API Key loaded: {masked}")
            print("✓ Configuration valid!\n")
            return True
        else:
            print("✗ Configuration invalid")
            return False
            
    except Exception as e:
        print(f"✗ Error verifying: {e}")
        return False

def main():
    print_banner()
    
    # Check if .env already exists with valid key
    if Path(".env").exists():
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            
            placeholder_keys = [
                "your_google_api_key_here",
                "your_api_key_here",
                "your_key_here",
                "your_actual_key_here",
            ]
            
            if api_key and api_key not in placeholder_keys and "your" not in api_key.lower() and api_key.startswith("AIza"):
                masked = api_key[:10] + "..." + api_key[-4:]
                print(f"✓ .env file already exists with valid key: {masked}\n")
                update = input("  Update it with a new key? (y/n): ").lower()
                if update != 'y':
                    print("\n✅ Using existing configuration.")
                    print("   Run 'python quick_test.py' to verify everything works.\n")
                    return
        except:
            pass
    
    # Get API key from user
    api_key = get_api_key()
    
    if not api_key:
        print("\n❌ Setup cancelled.\n")
        return
    
    # Create .env file
    if create_env_file(api_key):
        # Verify
        if verify_setup():
            print("="*60)
            print("   ✅ Setup Complete!")
            print("="*60 + "\n")
            print("Next steps:")
            print("   1. Run tests: python quick_test.py")
            print("   2. Start backend: python main.py\n")
        else:
            print("\n❌ Setup verification failed.")
            print("   Please check your .env file manually.\n")
    else:
        print("\n⚠️  .env file not created.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

