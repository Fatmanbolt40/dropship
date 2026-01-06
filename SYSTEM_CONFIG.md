# 🔐 SYSTEM CONFIGURATION & API KEYS
**Last Updated: January 2, 2026**

## 🌐 LIVE URLs
- **Public Store**: https://locomotively-needy-crysta.ngrok-free.dev
- **Backend API**: http://localhost:8000
- **Ngrok Status**: https://dashboard.ngrok.com

## 🔑 CRITICAL API KEYS & CREDENTIALS

### AI Services (ACTIVE)
```
OPENAI_API_KEY=your_openai_api_key_here

ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Amazon Services (ACTIVE)
```
AMAZON_AFFILIATE_TAG=legend0ee-20
AMAZON_EMAIL=gaminggodly@gmail.com
AMAZON_PASSWORD=Gamingkid22!
```
**Status**: Affiliate tag working ✅, Auto-purchase credentials stored

### Payment Processing (NOT CONFIGURED)
```
STRIPE_API_KEY=<NOT SET>
```
**Status**: Required for Phase 2 - Customer payments

### E-Commerce Platforms (NOT CONFIGURED)
```
SHOPIFY_API_KEY=<NOT SET>
SHOPIFY_API_SECRET=<NOT SET>
SHOPIFY_STORE_URL=<NOT SET>
```
**Status**: Optional - Currently using custom frontend

### Supplier APIs (NOT CONFIGURED)
```
ALIEXPRESS_API_KEY=<NOT SET>
ALIEXPRESS_API_SECRET=<NOT SET>
CJ_API_KEY=<NOT SET>
```
**Status**: Using web scraping instead

## 📦 CURRENT PRODUCT INVENTORY

### Live Products (5 Total)
1. **Amazon Basics Lightning Cable** (ASIN: B0BZWCCL7J)
   - Cost: $7.99 → Sell: $19.18 | Profit: $11.19
   
2. **Amazon Basics USB-C Cable** (ASIN: B0BZWCRXXL)
   - Cost: $8.99 → Sell: $21.58 | Profit: $12.59
   
3. **Blink Mini Security Camera** (ASIN: B08J8FFJ8H)
   - Cost: $34.99 → Sell: $73.48 | Profit: $38.49
   
4. **Fire TV Stick 4K Max** (ASIN: B09B8RRQTY)
   - Cost: $59.99 → Sell: $125.98 | Profit: $65.99
   
5. **Echo Dot (5th Gen)** (ASIN: B0D1XD1ZV3)
   - Cost: $49.99 → Sell: $104.98 | Profit: $54.99

**All ASINs verified real on Amazon.com ✅**

## 🛠️ TECHNICAL INFRASTRUCTURE

### Backend Stack
- FastAPI (Python 3.10+)
- uvicorn server on port 8000
- SQLite database: `dropship.db`
- Ngrok tunnel for public access

### Key Files
- `/home/Thalegendgamer/dropship/server.py` - Main API server
- `/home/Thalegendgamer/dropship/.env` - Environment variables
- `/home/Thalegendgamer/dropship/campaigns/` - Product database (JSON)
- `/home/Thalegendgamer/dropship/real_product_scraper.py` - Product sourcing

### Dependencies
- OpenAI Python SDK
- Anthropic Python SDK
- FastAPI + uvicorn
- python-dotenv
- Selenium (for auto-purchase bot)

## ⚠️ WHAT'S MISSING FOR AUTOMATION

### Phase 1: Payment Processing
- [ ] Stripe API integration
- [ ] Payment capture workflow
- [ ] Refund handling
- [ ] Tax calculation

### Phase 2: Amazon Auto-Purchase
- [ ] Amazon SP-API access (requires Amazon approval)
- [ ] Alternative: Selenium-based automation (risky - violates TOS)
- [ ] Order placement automation
- [ ] Tracking number extraction
- [ ] Error handling & retries

### Phase 3: Customer Experience
- [ ] Order confirmation emails
- [ ] Tracking updates
- [ ] Customer support system
- [ ] Fraud detection

### Phase 4: Legal & Compliance
- [ ] Business license
- [ ] Sales tax collection
- [ ] Terms of service
- [ ] Privacy policy
- [ ] Return/refund policy

## 🎯 CURRENT CAPABILITIES
✅ AI product research (OpenAI + Claude)
✅ Real Amazon products with verified ASINs
✅ Affiliate link generation
✅ Price markup calculation
✅ API serving product catalog
✅ Ngrok public access

## 🚫 NOT YET FUNCTIONAL
❌ Customer payment processing
❌ Automatic Amazon purchases
❌ Order tracking
❌ Email notifications
❌ Refunds/returns
❌ Legal compliance framework

## 💡 NEXT STEPS TO FULL AUTOMATION
See `AUTOMATION_MASTER_PLAN.md` for detailed roadmap.
