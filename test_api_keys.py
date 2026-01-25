#!/usr/bin/env python3
"""
Test All Your API Keys
Verifies Claude and Stripe are working correctly
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_claude():
    """Test Claude AI"""
    print("\n" + "="*60)
    print("🤖 TESTING CLAUDE AI")
    print("="*60)
    
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or 'your' in api_key.lower():
            print("❌ Claude API key not configured")
            return False
        
        print(f"✅ API Key: {api_key[:20]}...{api_key[-10:]}")
        
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'Claude API Working!' in one sentence."}]
        )
        
        print(f"✅ CLAUDE WORKING: {message.content[0].text}")
        print(f"💰 Cost: ~$0.0003 per request (very cheap!)")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_stripe():
    """Test Stripe Payments"""
    print("\n" + "="*60)
    print("💳 TESTING STRIPE PAYMENTS")
    print("="*60)
    
    try:
        import stripe
        
        api_key = os.getenv('STRIPE_API_KEY') or os.getenv('STRIPE_SECRET_KEY')
        if not api_key or 'your' in api_key.lower():
            print("❌ Stripe API key not configured")
            return False
        
        print(f"✅ API Key: {api_key[:20]}...{api_key[-10:]}")
        
        stripe.api_key = api_key
        
        # Test with a simple API call
        balance = stripe.Balance.retrieve()
        
        print(f"✅ STRIPE WORKING!")
        print(f"   Account Mode: {'LIVE' if 'live' in api_key else 'TEST'}")
        print(f"   Available Balance: ${balance.available[0].amount / 100:.2f} {balance.available[0].currency.upper()}")
        
        if 'live' in api_key:
            print("\n⚠️  WARNING: Using LIVE API key - real money!")
            print("   Make sure to test thoroughly before accepting real payments")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        if "Invalid API Key" in str(e):
            print("\n💡 Your Stripe key might be invalid or expired")
            print("   Get a new one at: https://dashboard.stripe.com/apikeys")
        return False

def test_sendgrid():
    """Test SendGrid Email"""
    print("\n" + "="*60)
    print("📧 CHECKING SENDGRID EMAIL")
    print("="*60)
    
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key or 'your' in api_key.lower():
        print("⚠️  SendGrid not configured yet")
        print("   Get free API key at: https://sendgrid.com")
        print("   Needed for: Order confirmations, shipping updates")
        return False
    
    print(f"✅ SendGrid configured: {api_key[:15]}...")
    return True

def main():
    print("\n🧪 API KEY VERIFICATION TEST")
    print("="*60)
    
    results = {
        'Claude AI': test_claude(),
        'Stripe Payments': test_stripe(),
        'SendGrid Email': test_sendgrid()
    }
    
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    
    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {service}: {'WORKING' if status else 'NOT CONFIGURED'}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print("\n" + "="*60)
    print(f"🎯 {working_count}/{total_count} CRITICAL SERVICES READY")
    print("="*60)
    
    if working_count >= 2:
        print("\n🚀 YOU CAN START ACCEPTING ORDERS!")
        print("   - Claude: Generate product descriptions")
        print("   - Stripe: Accept payments")
        print("   - Next: Add SendGrid for email notifications")
    else:
        print("\n⚠️  Need at least Claude + Stripe to go live")
        print("   Add missing API keys to .env file")
    
    print("\n")

if __name__ == "__main__":
    main()
