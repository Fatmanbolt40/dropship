import os
import stripe
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Stripe API configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_YOUR_KEY_HERE')

class PaymentProcessor:
    """Handle real payment processing with Stripe"""
    
    def __init__(self):
        self.stripe = stripe
    
    def create_checkout_session(self, product_data: dict, success_url: str, cancel_url: str):
        """
        Create a Stripe checkout session for a product
        
        Args:
            product_data: Dict with name, price (in cents), quantity, image
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment cancelled
        
        Returns:
            Stripe checkout session URL
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_data['name'],
                            'images': [product_data.get('image', '')],
                        },
                        'unit_amount': int(product_data['price'] * 100),  # Convert to cents
                    },
                    'quantity': product_data.get('quantity', 1),
                }],
                mode='payment',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={
                    'product_id': product_data.get('product_id', ''),
                    'supplier_url': product_data.get('supplier_url', ''),
                    'buy_price': product_data.get('buy_price', 0),
                }
            )
            return session.url
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Payment error: {str(e)}")
    
    def verify_payment(self, session_id: str):
        """
        Verify a payment was successful
        
        Args:
            session_id: Stripe checkout session ID
        
        Returns:
            Dict with payment details and metadata
        """
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                return {
                    'status': 'paid',
                    'amount_total': session.amount_total / 100,  # Convert from cents
                    'customer_email': session.customer_details.email,
                    'metadata': session.metadata,
                    'payment_intent': session.payment_intent
                }
            else:
                return {
                    'status': session.payment_status,
                    'amount_total': 0
                }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Verification error: {str(e)}")
    
    def create_payment_intent(self, amount: float, currency: str = 'usd', metadata: dict = None):
        """
        Create a payment intent (more flexible than checkout sessions)
        
        Args:
            amount: Amount in dollars
            currency: Currency code
            metadata: Additional data to attach
        
        Returns:
            Payment intent client secret
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True}
            )
            return {
                'client_secret': intent.client_secret,
                'intent_id': intent.id
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Payment intent error: {str(e)}")

# Initialize global processor
payment_processor = PaymentProcessor()
