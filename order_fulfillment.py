import json
import os
from datetime import datetime
from cj_api import CJDropshippingAPI
from dotenv import load_dotenv

load_dotenv()

class OrderFulfillment:
    """Handle order fulfillment workflow"""
    
    def __init__(self):
        self.cj_api = CJDropshippingAPI(
            email=os.getenv('CJ_EMAIL'),
            api_key=os.getenv('CJ_API_KEY')
        )
        self.orders_file = 'orders.json'
        self._ensure_orders_file()
    
    def _ensure_orders_file(self):
        """Create orders file if it doesn't exist"""
        if not os.path.exists(self.orders_file):
            with open(self.orders_file, 'w') as f:
                json.dump([], f)
    
    def create_order(self, payment_data: dict, product_data: dict, customer_data: dict):
        """
        Create order after successful payment
        
        Workflow:
        1. Customer pays you (via Stripe)
        2. Order product from CJ Dropshipping
        3. CJ ships directly to customer
        4. You keep the profit
        
        Args:
            payment_data: Payment info from Stripe
            product_data: Product details
            customer_data: Customer shipping info
        
        Returns:
            Order confirmation
        """
        order = {
            'order_id': f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'customer': customer_data,
            'product': product_data,
            'payment': {
                'amount_received': payment_data['amount_total'],
                'payment_intent': payment_data.get('payment_intent'),
                'status': payment_data['status']
            },
            'fulfillment': {
                'status': 'pending',
                'cj_order_id': None,
                'tracking_number': None
            },
            'profit': payment_data['amount_total'] - product_data.get('buy_price', 0)
        }
        
        # Save order
        orders = self._load_orders()
        orders.append(order)
        self._save_orders(orders)
        
        return order
    
    def process_cj_order(self, order_id: str):
        """
        Place order with CJ Dropshipping
        
        NOTE: This requires CJ API order placement endpoint
        For now, this logs the order for manual processing
        
        Args:
            order_id: Your order ID
        
        Returns:
            CJ order confirmation
        """
        orders = self._load_orders()
        order = next((o for o in orders if o['order_id'] == order_id), None)
        
        if not order:
            return {'error': 'Order not found'}
        
        # TODO: Implement CJ API order placement
        # For now, mark as ready for manual processing
        order['fulfillment']['status'] = 'ready_for_cj'
        order['fulfillment']['notes'] = (
            f"READY TO ORDER FROM CJ:\n"
            f"Product: {order['product']['name']}\n"
            f"CJ URL: {order['product'].get('supplier_url')}\n"
            f"Customer: {order['customer'].get('email')}\n"
            f"Address: {order['customer'].get('address')}\n"
            f"Amount to spend: ${order['product'].get('buy_price', 0)}\n"
            f"You received: ${order['payment']['amount_received']}\n"
            f"Your profit: ${order['profit']}"
        )
        
        self._save_orders(orders)
        return order
    
    def get_order(self, order_id: str):
        """Get order details"""
        orders = self._load_orders()
        return next((o for o in orders if o['order_id'] == order_id), None)
    
    def list_orders(self, status: str = None):
        """List all orders, optionally filtered by status"""
        orders = self._load_orders()
        if status:
            return [o for o in orders if o['fulfillment']['status'] == status]
        return orders
    
    def _load_orders(self):
        """Load orders from file"""
        try:
            with open(self.orders_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_orders(self, orders):
        """Save orders to file"""
        with open(self.orders_file, 'w') as f:
            json.dump(orders, f, indent=2)

# Initialize global fulfillment handler
order_fulfillment = OrderFulfillment()
