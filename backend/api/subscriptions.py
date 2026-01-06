#!/usr/bin/env python3
"""
Subscription & API Key Management System
Stripe integration for bi-weekly, monthly, and yearly subscriptions
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
import stripe
import os
import json
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Stripe configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_key_here')

# Subscription Plans
SUBSCRIPTION_PLANS = {
    'starter_biweekly': {
        'name': 'Starter (Bi-Weekly)',
        'price': 19.99,
        'interval': 'biweekly',
        'features': ['100 products/day', 'Basic AI', '5 campaigns/month'],
        'rate_limit': 100,
        'stripe_price_id': 'price_starter_biweekly'
    },
    'starter_monthly': {
        'name': 'Starter (Monthly)',
        'price': 39.99,
        'interval': 'month',
        'features': ['100 products/day', 'Basic AI', '5 campaigns/month'],
        'rate_limit': 100,
        'stripe_price_id': 'price_starter_monthly'
    },
    'starter_yearly': {
        'name': 'Starter (Yearly)',
        'price': 399.99,
        'interval': 'year',
        'features': ['100 products/day', 'Basic AI', '5 campaigns/month'],
        'rate_limit': 100,
        'stripe_price_id': 'price_starter_yearly'
    },
    'pro_biweekly': {
        'name': 'Pro (Bi-Weekly)',
        'price': 49.99,
        'interval': 'biweekly',
        'features': ['500 products/day', 'Advanced AI', '25 campaigns/month', 'Priority support'],
        'rate_limit': 500,
        'stripe_price_id': 'price_pro_biweekly'
    },
    'pro_monthly': {
        'name': 'Pro (Monthly)',
        'price': 99.99,
        'interval': 'month',
        'features': ['500 products/day', 'Advanced AI', '25 campaigns/month', 'Priority support'],
        'rate_limit': 500,
        'stripe_price_id': 'price_pro_monthly'
    },
    'pro_yearly': {
        'name': 'Pro (Yearly)',
        'price': 999.99,
        'interval': 'year',
        'features': ['500 products/day', 'Advanced AI', '25 campaigns/month', 'Priority support'],
        'rate_limit': 500,
        'stripe_price_id': 'price_pro_yearly'
    },
    'enterprise_biweekly': {
        'name': 'Enterprise (Bi-Weekly)',
        'price': 99.99,
        'interval': 'biweekly',
        'features': ['Unlimited products', 'Premium AI (GPT-4)', 'Unlimited campaigns', 'Dedicated support', 'Custom integrations'],
        'rate_limit': 10000,
        'stripe_price_id': 'price_enterprise_biweekly'
    },
    'enterprise_monthly': {
        'name': 'Enterprise (Monthly)',
        'price': 199.99,
        'interval': 'month',
        'features': ['Unlimited products', 'Premium AI (GPT-4)', 'Unlimited campaigns', 'Dedicated support', 'Custom integrations'],
        'rate_limit': 10000,
        'stripe_price_id': 'price_enterprise_monthly'
    },
    'enterprise_yearly': {
        'name': 'Enterprise (Yearly)',
        'price': 1999.99,
        'interval': 'year',
        'features': ['Unlimited products', 'Premium AI (GPT-4)', 'Unlimited campaigns', 'Dedicated support', 'Custom integrations'],
        'rate_limit': 10000,
        'stripe_price_id': 'price_enterprise_yearly'
    }
}

# In-memory storage (use database in production)
API_KEYS_DB = {}
SUBSCRIPTIONS_DB = {}

class SubscriptionRequest(BaseModel):
    email: EmailStr
    plan_id: str
    payment_method_id: str

class APIKeyResponse(BaseModel):
    api_key: str
    subscription_plan: str
    expires_at: str
    rate_limit: int

def generate_api_key() -> str:
    """Generate a secure API key"""
    return f"sk_live_{secrets.token_urlsafe(32)}"

def verify_api_key(api_key: str = Header(None, alias="X-API-Key")) -> dict:
    """Verify API key and return user info"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if api_key not in API_KEYS_DB:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    user_data = API_KEYS_DB[api_key]
    
    # Check if subscription is active
    if datetime.fromisoformat(user_data['expires_at']) < datetime.now():
        raise HTTPException(status_code=403, detail="Subscription expired")
    
    return user_data

@router.get("/api/subscription/plans")
async def get_plans():
    """Get all available subscription plans"""
    return {
        "success": True,
        "plans": SUBSCRIPTION_PLANS
    }

@router.post("/api/subscription/create")
async def create_subscription(request: SubscriptionRequest):
    """Create a new subscription and generate API key"""
    try:
        plan = SUBSCRIPTION_PLANS.get(request.plan_id)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan ID")
        
        # Create Stripe customer
        customer = stripe.Customer.create(
            email=request.email,
            payment_method=request.payment_method_id,
            invoice_settings={'default_payment_method': request.payment_method_id}
        )
        
        # Create Stripe subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': plan['stripe_price_id']}],
            expand=['latest_invoice.payment_intent']
        )
        
        # Generate API key
        api_key = generate_api_key()
        
        # Calculate expiration
        if plan['interval'] == 'biweekly':
            expires_at = datetime.now() + timedelta(days=14)
        elif plan['interval'] == 'month':
            expires_at = datetime.now() + timedelta(days=30)
        else:  # yearly
            expires_at = datetime.now() + timedelta(days=365)
        
        # Store subscription data
        user_data = {
            'email': request.email,
            'plan_id': request.plan_id,
            'subscription_id': subscription.id,
            'customer_id': customer.id,
            'rate_limit': plan['rate_limit'],
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'status': 'active'
        }
        
        API_KEYS_DB[api_key] = user_data
        SUBSCRIPTIONS_DB[subscription.id] = api_key
        
        # Save to file (backup)
        save_subscriptions()
        
        return {
            "success": True,
            "api_key": api_key,
            "subscription": {
                "plan": plan['name'],
                "price": plan['price'],
                "interval": plan['interval'],
                "expires_at": expires_at.isoformat(),
                "rate_limit": plan['rate_limit']
            }
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/subscription/status")
async def get_subscription_status(user_data: dict = Depends(verify_api_key)):
    """Get current subscription status"""
    plan = SUBSCRIPTION_PLANS.get(user_data['plan_id'])
    
    return {
        "success": True,
        "subscription": {
            "email": user_data['email'],
            "plan": plan['name'] if plan else 'Unknown',
            "status": user_data['status'],
            "expires_at": user_data['expires_at'],
            "rate_limit": user_data['rate_limit'],
            "features": plan['features'] if plan else []
        }
    }

@router.post("/api/subscription/cancel")
async def cancel_subscription(user_data: dict = Depends(verify_api_key)):
    """Cancel subscription"""
    try:
        subscription_id = user_data.get('subscription_id')
        if subscription_id:
            stripe.Subscription.delete(subscription_id)
        
        user_data['status'] = 'cancelled'
        save_subscriptions()
        
        return {
            "success": True,
            "message": "Subscription cancelled successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/webhook/stripe")
async def stripe_webhook(request: dict):
    """Handle Stripe webhooks for subscription events"""
    event_type = request.get('type')
    
    if event_type == 'customer.subscription.deleted':
        subscription_id = request['data']['object']['id']
        if subscription_id in SUBSCRIPTIONS_DB:
            api_key = SUBSCRIPTIONS_DB[subscription_id]
            if api_key in API_KEYS_DB:
                API_KEYS_DB[api_key]['status'] = 'cancelled'
    
    elif event_type == 'invoice.payment_succeeded':
        subscription_id = request['data']['object']['subscription']
        if subscription_id in SUBSCRIPTIONS_DB:
            api_key = SUBSCRIPTIONS_DB[subscription_id]
            if api_key in API_KEYS_DB:
                # Extend subscription
                user_data = API_KEYS_DB[api_key]
                plan = SUBSCRIPTION_PLANS.get(user_data['plan_id'])
                
                if plan['interval'] == 'biweekly':
                    new_expiry = datetime.now() + timedelta(days=14)
                elif plan['interval'] == 'month':
                    new_expiry = datetime.now() + timedelta(days=30)
                else:
                    new_expiry = datetime.now() + timedelta(days=365)
                
                user_data['expires_at'] = new_expiry.isoformat()
                user_data['status'] = 'active'
    
    save_subscriptions()
    return {"success": True}

def save_subscriptions():
    """Save subscriptions to file"""
    with open('subscriptions.json', 'w') as f:
        json.dump({
            'api_keys': API_KEYS_DB,
            'subscriptions': SUBSCRIPTIONS_DB
        }, f, indent=2)

def load_subscriptions():
    """Load subscriptions from file"""
    global API_KEYS_DB, SUBSCRIPTIONS_DB
    try:
        if os.path.exists('subscriptions.json'):
            with open('subscriptions.json', 'r') as f:
                data = json.load(f)
                API_KEYS_DB = data.get('api_keys', {})
                SUBSCRIPTIONS_DB = data.get('subscriptions', {})
    except Exception as e:
        print(f"Error loading subscriptions: {e}")

# Load existing subscriptions on startup
load_subscriptions()

# Export router
subscription_router = router
