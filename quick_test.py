"""
Simple AI Test - Debug API Keys
"""

import os

# Your API keys - load from environment variables
OPENAI_KEY = os.getenv('OPENAI_API_KEY', 'your_key_here')
CLAUDE_KEY = os.getenv('ANTHROPIC_API_KEY', 'your_key_here')

print("🔍 Testing API Keys...")
print("=" * 60)

# Test OpenAI
print("\n1️⃣ Testing OpenAI...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    
    # Try to list models to verify key works
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello'"}],
        max_tokens=10
    )
    print(f"✅ OpenAI: WORKING! Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI Error: {str(e)[:200]}")

# Test Claude
print("\n2️⃣ Testing Claude...")
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=CLAUDE_KEY)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Say 'Hello'"}]
    )
    print(f"✅ Claude: WORKING! Response: {message.content[0].text}")
except Exception as e:
    print(f"❌ Claude Error: {str(e)[:200]}")

print("\n" + "=" * 60)
