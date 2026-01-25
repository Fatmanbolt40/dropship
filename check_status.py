#!/usr/bin/env python3
"""
🎯 SYSTEM STATUS DASHBOARD
Shows what's configured and what's missing
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_api(name, key_name, required=True):
    """Check if API key is configured"""
    key = os.getenv(key_name)
    if key and key != f'your_{key_name.lower()}' and 'YOUR' not in key:
        masked = f"{key[:20]}...{key[-10:]}" if len(key) > 30 else key[:15]+"..."
        return True, masked
    return False, None

print("\n" + "="*70)
print("🚀 DROPSHIPPING SYSTEM STATUS")
print("="*70)

# Critical APIs
print("\n🔴 CRITICAL (Must Have to Go Live):")
print("-"*70)

status, key = check_api("Claude AI", "ANTHROPIC_API_KEY")
print(f"{'✅' if status else '❌'} Claude AI: {'READY' if status else 'MISSING'}")
if status:
    print(f"   Key: {key}")
    print(f"   Model: {os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')}")
    print(f"   Cost: ~95% cheaper than OpenAI!")

status, key = check_api("Stripe Secret", "STRIPE_SECRET_KEY")
print(f"\n{'✅' if status else '❌'} Stripe Payments: {'READY' if status else 'MISSING'}")
if status:
    print(f"   Secret: {key}")
    status2, key2 = check_api("Stripe Publishable", "STRIPE_PUBLISHABLE_KEY")
    if status2:
        print(f"   Publishable: {key2}")
        print(f"   Mode: {'LIVE ⚠️ ' if 'live' in key else 'TEST'}Real money!")

status, key = check_api("SendGrid", "SENDGRID_API_KEY")
print(f"\n{'✅' if status else '❌'} SendGrid Email: {'READY' if status else 'MISSING ⚠️'}")
if status:
    print(f"   Key: {key}")
    print(f"   From: {os.getenv('FROM_EMAIL', 'Not set')}")
else:
    print(f"   Get FREE at: https://sendgrid.com")
    print(f"   Needed for: Order confirmations, shipping updates")

# Product Sourcing
print("\n🟡 PRODUCT SOURCING:")
print("-"*70)

status, key = check_api("CJ Dropshipping", "CJ_API_KEY")
print(f"{'✅' if status else '❌'} CJ Dropshipping: {'READY' if status else 'MISSING'}")
if status:
    print(f"   Email: {os.getenv('CJ_EMAIL', 'Not set')}")
    print(f"   Key: {key}")
else:
    print(f"   Get at: https://cjdropshipping.com")
    print(f"   Needed for: Auto-fulfillment & shipping")

status, key = check_api("Amazon Affiliate", "AMAZON_AFFILIATE_TAG")
print(f"\n{'✅' if status else '❌'} Amazon Affiliate: {'READY' if status else 'MISSING'}")
if status:
    print(f"   Tag: {os.getenv('AMAZON_AFFILIATE_TAG')}")
    print(f"   Earn: 3-10% commission per sale")

# Optional APIs
print("\n🟢 OPTIONAL (Nice to Have):")
print("-"*70)

status, key = check_api("Google Analytics", "GOOGLE_ANALYTICS_ID")
print(f"{'✅' if status else '⚪'} Google Analytics: {'READY' if status else 'Not configured'}")

status, key = check_api("Facebook", "FACEBOOK_ACCESS_TOKEN")
print(f"{'✅' if status else '⚪'} Facebook Marketing: {'READY' if status else 'Not configured'}")

status, key = check_api("Shopify", "SHOPIFY_API_KEY")
print(f"{'✅' if status else '⚪'} Shopify: {'READY' if status else 'Not configured'}")

# Calculate readiness
print("\n" + "="*70)
print("📊 READINESS SCORE")
print("="*70)

critical = []
claude_ready, _ = check_api("Claude", "ANTHROPIC_API_KEY")
stripe_ready, _ = check_api("Stripe", "STRIPE_SECRET_KEY")
stripe_pub_ready, _ = check_api("Stripe Pub", "STRIPE_PUBLISHABLE_KEY")
sendgrid_ready, _ = check_api("SendGrid", "SENDGRID_API_KEY")
cj_ready, _ = check_api("CJ", "CJ_API_KEY")

critical.append(("Claude AI", claude_ready))
critical.append(("Stripe Payments", stripe_ready and stripe_pub_ready))
critical.append(("Email Notifications", sendgrid_ready))
critical.append(("Product Fulfillment", cj_ready))

ready_count = sum(1 for _, ready in critical for ready in [ready] if ready)
total_count = len(critical)

for name, ready in critical:
    print(f"{'✅' if ready else '❌'} {name}")

print(f"\n🎯 {ready_count}/{total_count} Critical Services Ready")

if ready_count >= 3:
    print("\n✅ SYSTEM READY TO LAUNCH!")
    print("   You can start accepting orders now!")
    if not sendgrid_ready:
        print("   ⚠️  Add SendGrid for email notifications")
    if not cj_ready:
        print("   ⚠️  Add CJ Dropshipping for auto-fulfillment")
elif ready_count >= 2:
    print("\n⚠️  ALMOST READY!")
    print("   Add missing APIs to go fully autonomous")
else:
    print("\n❌ NOT READY")
    print("   Configure critical APIs first")

print("\n" + "="*70)
print("💡 NEXT STEPS:")
print("="*70)

if not sendgrid_ready:
    print("1. Get SendGrid (FREE): https://sendgrid.com")
    print("   → Settings → API Keys → Create API Key")
    print("   → Add to .env: SENDGRID_API_KEY=SG.xxx")

if not cj_ready:
    print("2. Get CJ Dropshipping: https://cjdropshipping.com")
    print("   → Sign up → Profile → API Settings")
    print("   → Add to .env: CJ_EMAIL and CJ_API_KEY")

if ready_count >= 2:
    print("\n3. Test your system:")
    print("   python3 server.py")
    print("   Visit: http://localhost:8000")

print("\n" + "="*70)
print()
