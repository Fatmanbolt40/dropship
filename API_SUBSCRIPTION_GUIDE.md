# 💰 AI Dropshipping API - Subscription Service

Your AI dropshipping automation is now available as a subscription API!

## 🎯 Pricing Plans

### Starter
- **Bi-Weekly:** $19.99/2 weeks
- **Monthly:** $39.99/month
- **Yearly:** $399.99/year (Save 20%)

**Features:**
- 100 products/day
- Basic AI (GPT-3.5)
- 5 campaigns/month
- Email support
- API access (100 requests/hour)

### Pro (Most Popular)
- **Bi-Weekly:** $49.99/2 weeks
- **Monthly:** $99.99/month
- **Yearly:** $999.99/year (Save 20%)

**Features:**
- 500 products/day
- Advanced AI (GPT-4)
- 25 campaigns/month
- Priority support
- API access (500 requests/hour)
- Advanced analytics

### Enterprise
- **Bi-Weekly:** $99.99/2 weeks
- **Monthly:** $199.99/month
- **Yearly:** $1,999.99/year (Save 20%)

**Features:**
- Unlimited products
- Premium AI (GPT-4 + Claude)
- Unlimited campaigns
- Dedicated support
- API access (10,000 requests/hour)
- Custom integrations

---

## 🔑 API Authentication

All API requests require an API key in the header:

```bash
curl -H "X-API-Key: sk_live_your_api_key" \
     https://your-api.com/api/products/find
```

---

## 📡 API Endpoints

### Product Finding
```
POST /api/products/find
GET /api/products/trending
GET /api/products/{product_id}
```

### Marketing
```
POST /api/marketing/campaign/create
GET /api/marketing/campaigns
POST /api/social/post
```

### Automation
```
POST /api/automation/start
GET /api/automation/status
POST /api/automation/config
```

### Subscriptions
```
GET /api/subscription/plans
POST /api/subscription/create
GET /api/subscription/status
POST /api/subscription/cancel
```

---

## 🚀 Quick Start

### 1. Subscribe
```javascript
// Visit pricing page
window.location.href = '/pricing.html';

// Or use API
const response = await fetch('/api/subscription/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    plan_id: 'pro_monthly',
    payment_method_id: 'pm_xxx' // Stripe payment method
  })
});

const { api_key } = await response.json();
```

### 2. Use API
```python
import requests

API_KEY = "sk_live_your_api_key"
headers = {"X-API-Key": API_KEY}

# Find trending products
response = requests.post(
    "https://your-api.com/api/products/find",
    headers=headers,
    json={"niche": "electronics", "max_price": 100}
)

products = response.json()
```

### 3. Monitor Usage
```bash
# Check rate limits
curl -H "X-API-Key: sk_live_your_key" \
     https://your-api.com/api/subscription/status

# Response includes:
# X-RateLimit-Limit: 500
# X-RateLimit-Remaining: 450
# X-RateLimit-Reset: 1704567890
```

---

## 💳 Payment Integration

### Stripe Setup
```bash
# Add to .env
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
```

### Webhook Configuration
```
Stripe Dashboard → Webhooks → Add endpoint
URL: https://your-api.com/api/webhook/stripe
Events: 
  - customer.subscription.deleted
  - invoice.payment_succeeded
  - invoice.payment_failed
```

---

## 🔒 Security

- API keys are hashed and stored securely
- Rate limiting prevents abuse
- Stripe handles all payment processing
- HTTPS required for all requests
- Webhook signature verification

---

## 📊 Rate Limits

| Plan | Requests/Hour | Requests/Day |
|------|--------------|--------------|
| Starter | 100 | 2,400 |
| Pro | 500 | 12,000 |
| Enterprise | 10,000 | 240,000 |

**429 Response (Rate Limit Exceeded):**
```json
{
  "error": "Rate limit exceeded",
  "limit": 500,
  "reset_at": "2026-01-05T21:00:00Z"
}
```

---

## 🎨 Frontend Integration

Add to your dashboard:
```html
<a href="/pricing.html" class="btn">Upgrade to Pro</a>
```

Or embed in-app:
```javascript
// Check subscription status
async function checkSubscription() {
  const response = await fetch('/api/subscription/status', {
    headers: { 'X-API-Key': localStorage.getItem('api_key') }
  });
  const { subscription } = await response.json();
  
  if (subscription.plan === 'Starter') {
    showUpgradePrompt();
  }
}
```

---

## 📈 Revenue Projections

**10 subscribers (Starter):** $400/month  
**50 subscribers (Pro avg):** $5,000/month  
**100 subscribers (Mixed):** $10,000+/month  

**Yearly customers:** 20% discount = more stable revenue  
**Bi-weekly:** More frequent touchpoints, less churn  

---

## 🔧 Technical Setup

### 1. Backend
```bash
cd backend
pip install stripe
python main.py
```

### 2. Create Stripe Products
```bash
# In Stripe Dashboard, create products with IDs:
# - price_starter_biweekly
# - price_starter_monthly
# - price_starter_yearly
# (repeat for pro and enterprise)
```

### 3. Deploy
```bash
git add -A
git commit -m "Add subscription API"
git push
```

---

## 📞 Support

- **Email:** support@yourapi.com
- **Docs:** https://docs.yourapi.com
- **Discord:** discord.gg/yourapi

---

**Start monetizing your AI today!** 🚀💰
