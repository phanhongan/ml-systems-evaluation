import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def check_openai_model_access():
    """Utility script to check which OpenAI models are available with current API key"""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your-openai-api-key-here":
        print("❌ No valid API key found in .env file")
        return

    client = OpenAI(api_key=api_key)

    # Test different models
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-1106-preview",  # GPT-4.1 nano
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
    ]

    print("🔍 Testing OpenAI model access...")
    print("=" * 50)

    for model in models_to_test:
        try:
            # Try a simple completion to test access
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
            )
            print(f"✅ {model}: ACCESSIBLE")
        except Exception as e:
            error_msg = str(e)
            if "does not exist" in error_msg or "not found" in error_msg:
                print(f"❌ {model}: NOT AVAILABLE")
            elif "quota" in error_msg or "billing" in error_msg:
                print(f"⚠️  {model}: QUOTA/BILLING ISSUE")
            else:
                print(f"❌ {model}: ERROR - {error_msg[:50]}...")

    print("=" * 50)
    print("💡 If you see 'QUOTA/BILLING ISSUE', you need to:")
    print("   1. Add billing information to your OpenAI account")
    print("   2. Add credits to your account")
    print("   3. Upgrade to a paid plan if on free tier")


if __name__ == "__main__":
    check_openai_model_access()
