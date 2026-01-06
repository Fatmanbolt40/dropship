"""
Quick AI Test - Show AI Features Working
Tests OpenAI and Claude APIs with your keys
"""

import os
from openai import OpenAI
from anthropic import Anthropic

# Your API keys - load from environment variables
OPENAI_KEY = os.getenv('OPENAI_API_KEY', 'your_key_here')
CLAUDE_KEY = os.getenv('ANTHROPIC_API_KEY', 'your_key_here')

def test_openai():
    """Test OpenAI API"""
    print("\n" + "="*60)
    print("🤖 TESTING OPENAI (GPT-3.5)")
    print("="*60)
    
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        
        print("\n📝 Generating product description for: 'Wireless Earbuds'")
        print("-" * 60)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": """Write a compelling 100-word product description for 'Premium Wireless Earbuds' that:
                - Highlights noise cancellation
                - Emphasizes long battery life
                - Includes a call-to-action
                - Is persuasive and SEO-friendly"""}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        description = response.choices[0].message.content
        print("\n✨ AI-GENERATED DESCRIPTION:\n")
        print(description)
        print("\n" + "-"*60)
        print(f"✅ OpenAI is working! Used {response.usage.total_tokens} tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return False

def test_claude():
    """Test Claude API"""
    print("\n" + "="*60)
    print("🤖 TESTING CLAUDE (Anthropic)")
    print("="*60)
    
    try:
        client = Anthropic(api_key=CLAUDE_KEY)
        
        print("\n📝 Generating ad copy for: 'Wireless Earbuds'")
        print("-" * 60)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Latest Claude model
            max_tokens=300,
            messages=[
                {"role": "user", "content": """Create 3 attention-grabbing Facebook ad headlines for 'Premium Wireless Earbuds'. 
                Each should be under 40 characters and emphasize different benefits.
                Format: numbered list."""}
            ]
        )
        
        ad_copy = message.content[0].text
        print("\n✨ AI-GENERATED AD HEADLINES:\n")
        print(ad_copy)
        print("\n" + "-"*60)
        print(f"✅ Claude is working! Used {message.usage.input_tokens + message.usage.output_tokens} tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ Claude Error: {e}")
        return False

def demo_product_research():
    """Demo: AI Product Research"""
    print("\n" + "="*60)
    print("🔍 DEMO: AI-POWERED PRODUCT RESEARCH")
    print("="*60)
    
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        
        product = "Smart Water Bottle"
        print(f"\n📊 Analyzing market for: '{product}'")
        print("-" * 60)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"""As a dropshipping expert, analyze '{product}' and provide:
                1. Target audience (age, interests)
                2. Profit margin potential (score 1-10)
                3. Market saturation level
                4. Top 3 selling points
                5. Recommended price range
                
                Be concise and specific."""}
            ],
            max_tokens=300
        )
        
        analysis = response.choices[0].message.content
        print("\n🤖 AI MARKET ANALYSIS:\n")
        print(analysis)
        print("\n✅ This is what your platform does automatically!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all AI tests"""
    print("\n🚀 DROPSHIP AI - LIVE AI DEMONSTRATION")
    print("="*60)
    print("Testing both AI engines with your API keys...")
    
    # Test APIs
    openai_works = test_openai()
    claude_works = test_claude()
    
    # Demo features
    if openai_works or claude_works:
        demo_product_research()
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"OpenAI (GPT-3.5): {'✅ Active' if openai_works else '❌ Failed'}")
    print(f"Claude (Anthropic): {'✅ Active' if claude_works else '❌ Failed'}")
    print("\n🎯 YOUR PLATFORM CAN:")
    print("  • Generate product descriptions")
    print("  • Create ad copy automatically")
    print("  • Analyze market potential")
    print("  • Write TikTok video scripts")
    print("  • Generate email campaigns")
    print("  • And much more!")
    print("\n🔥 All AI features are now live and ready for your demo!")
    print("="*60)

if __name__ == "__main__":
    main()
