# Stripe Setup Instructions

## Step 1: Get Your Stripe API Keys

1. **Create Stripe Account** (FREE):
   - Go to https://stripe.com
   - Click "Start now" → Sign up
   - Verify your email
   - You can use TEST MODE immediately (no verification needed!)

2. **Get API Keys**:
   - Go to https://dashboard.stripe.com/test/apikeys
   - You'll see two keys:
     - **Publishable key** (starts with `pk_test_...`)
     - **Secret key** (starts with `sk_test_...`) - Click "Reveal" to see it

## Step 2: Add Keys to .env File

Open `/home/Thalegendgamer/dropship/.env` and add:

```bash
# Stripe API Keys (TEST MODE - no real money charged)
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
```

## Step 3: Install Stripe Library

```bash
cd /home/Thalegendgamer/dropship
./venv/bin/pip install stripe
```

## Step 4: Restart Your Server

```bash
# Kill current server
pkill -f "python.*server.py"

# Start new server with payment support
./venv/bin/python server.py
```

## How It Works (Your Dropshipping Workflow):

### WITHOUT Stripe (Current - Simulation Only):
❌ Customer clicks "Buy" → Nothing happens → Fake sales counter
❌ No real money received

### WITH Stripe (Real Money):
1. ✅ Customer clicks "Buy" → Redirected to Stripe checkout page
2. ✅ Customer enters credit card → Stripe processes payment
3. ✅ **YOU RECEIVE MONEY** in your Stripe account (minus 2.9% + $0.30 fee)
4. ✅ System creates order → Shows you which product to order from CJ
5. ✅ You log into CJ Dropshipping → Order the product (spend $X)
6. ✅ CJ ships directly to customer
7. ✅ **YOU KEEP THE PROFIT!**

## Example Transaction:

- Customer pays you: **$54.98** (via Stripe)
- Stripe fee (2.9% + $0.30): **-$1.89**
- You receive: **$53.09**
- You order from CJ: **-$18.50**
- **YOUR PROFIT: $34.59** 💰

## Test Mode vs Live Mode:

**TEST MODE** (what you'll use first):
- Uses fake credit card: `4242 4242 4242 4242` (any future date, any CVC)
- No real money moves
- Perfect for testing and demos

**LIVE MODE** (when you're ready to sell):
- Stripe needs: Business verification, bank account
- Real credit cards charged
- Real money deposited to your bank account

## Next Steps:

1. Get Stripe keys (takes 2 minutes)
2. Add to `.env` file
3. Install `stripe` library
4. Restart server
5. Test with fake card `4242 4242 4242 4242`
6. Watch REAL checkout flow work!

---

**Need help?** Just ask and I'll guide you through each step!
