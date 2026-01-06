#!/usr/bin/env python3
"""
Amazon Auto-Purchase Bot
Automatically purchases products from Amazon when orders are placed
WARNING: This violates Amazon TOS - use at your own risk!
"""

import os
import time
import json
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv

load_dotenv()


class AmazonAutoBuyer:
    """Automated Amazon purchase bot using Selenium"""
    
    def __init__(self, headless=False):
        self.email = os.getenv('AMAZON_EMAIL')
        self.password = os.getenv('AMAZON_PASSWORD')
        self.headless = headless
        self.driver = None
        
        if not self.email or not self.password:
            raise ValueError("Amazon credentials not found in .env file")
    
    def _setup_driver(self):
        """Initialize Chrome WebDriver with anti-detection settings"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome driver initialized")
    
    def _human_delay(self, min_seconds=1, max_seconds=3):
        """Random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def _type_like_human(self, element, text):
        """Type text with random delays between keystrokes"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def login(self):
        """Log into Amazon account"""
        print("🔐 Logging into Amazon...")
        
        try:
            self.driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
            
            self._human_delay(2, 4)
            
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            self._type_like_human(email_input, self.email)
            
            # Click Continue
            continue_btn = self.driver.find_element(By.ID, "continue")
            self._human_delay()
            continue_btn.click()
            
            # Enter password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            self._type_like_human(password_input, self.password)
            
            # Click Sign In
            signin_btn = self.driver.find_element(By.ID, "signInSubmit")
            self._human_delay()
            signin_btn.click()
            
            # Wait for login to complete
            self._human_delay(3, 5)
            
            # Check for CAPTCHA or 2FA
            if "auth/approve" in self.driver.current_url or "ap/cvf" in self.driver.current_url:
                print("⚠️  2FA/CAPTCHA detected - waiting 60 seconds for manual intervention...")
                time.sleep(60)
            
            print("✅ Logged in successfully")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def add_to_cart(self, asin):
        """Add product to cart by ASIN"""
        print(f"🛒 Adding ASIN {asin} to cart...")
        
        try:
            # Navigate to product page
            product_url = f"https://www.amazon.com/dp/{asin}"
            self.driver.get(product_url)
            self._human_delay(2, 4)
            
            # Check if product exists
            if "Sorry, we couldn't find that page" in self.driver.page_source:
                raise Exception(f"Product {asin} not found")
            
            # Find and click "Add to Cart" button
            try:
                add_to_cart = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
                )
                self._human_delay()
                add_to_cart.click()
                print("✅ Added to cart")
                self._human_delay(2, 3)
                return True
                
            except TimeoutException:
                # Try alternative button IDs
                try:
                    add_to_cart = self.driver.find_element(By.NAME, "submit.add-to-cart")
                    add_to_cart.click()
                    print("✅ Added to cart (alternative method)")
                    self._human_delay(2, 3)
                    return True
                except:
                    raise Exception("Add to cart button not found")
            
        except Exception as e:
            print(f"❌ Failed to add to cart: {e}")
            return False
    
    def checkout(self, shipping_address):
        """Proceed to checkout and enter shipping address"""
        print("💳 Proceeding to checkout...")
        
        try:
            # Go to cart
            self.driver.get("https://www.amazon.com/gp/cart/view.html")
            self._human_delay(2, 3)
            
            # Click "Proceed to checkout"
            try:
                checkout_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "proceedToRetailCheckout"))
                )
                self._human_delay()
                checkout_btn.click()
            except:
                # Alternative checkout button
                checkout_btn = self.driver.find_element(By.ID, "sc-buy-box-ptc-button")
                checkout_btn.click()
            
            self._human_delay(3, 5)
            
            # Handle shipping address
            if self._is_new_address_needed(shipping_address):
                self._add_new_address(shipping_address)
            else:
                self._select_existing_address(shipping_address)
            
            # Continue to shipping options
            try:
                continue_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][aria-labelledby*='address']"))
                )
                self._human_delay()
                continue_btn.click()
            except:
                pass  # Might auto-proceed
            
            self._human_delay(3, 5)
            
            # Select fastest shipping
            self._select_shipping_method()
            
            # Continue to payment
            try:
                continue_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][aria-labelledby*='shipping']"))
                )
                self._human_delay()
                continue_btn.click()
            except:
                pass
            
            self._human_delay(3, 5)
            
            print("✅ Ready for payment")
            return True
            
        except Exception as e:
            print(f"❌ Checkout failed: {e}")
            return False
    
    def _is_new_address_needed(self, shipping_address):
        """Check if we need to add a new address"""
        # For now, always try to use existing addresses first
        return False
    
    def _select_existing_address(self, shipping_address):
        """Select an existing address or use default"""
        print("📍 Using existing shipping address...")
        # Amazon usually has default address selected
        pass
    
    def _add_new_address(self, shipping_address):
        """Add a new shipping address"""
        print("📍 Adding new shipping address...")
        
        try:
            # Click "Add new address"
            add_address_btn = self.driver.find_element(By.ID, "add-new-address-popover-link")
            add_address_btn.click()
            self._human_delay()
            
            # Fill address form
            name_input = self.driver.find_element(By.ID, "address-ui-widgets-enterAddressFullName")
            self._type_like_human(name_input, shipping_address.get('name', ''))
            
            street_input = self.driver.find_element(By.ID, "address-ui-widgets-enterAddressLine1")
            self._type_like_human(street_input, shipping_address.get('street', ''))
            
            city_input = self.driver.find_element(By.ID, "address-ui-widgets-enterAddressCity")
            self._type_like_human(city_input, shipping_address.get('city', ''))
            
            state_select = self.driver.find_element(By.ID, "address-ui-widgets-enterAddressStateOrRegion")
            state_select.send_keys(shipping_address.get('state', ''))
            
            zip_input = self.driver.find_element(By.ID, "address-ui-widgets-enterAddressPostalCode")
            self._type_like_human(zip_input, shipping_address.get('zip', ''))
            
            # Submit address
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[aria-labelledby='address-ui-widgets-form-submit-button']")
            self._human_delay()
            submit_btn.click()
            
            print("✅ New address added")
            self._human_delay(2, 3)
            
        except Exception as e:
            print(f"⚠️  Address add failed (may already exist): {e}")
    
    def _select_shipping_method(self):
        """Select fastest available shipping method"""
        print("🚚 Selecting shipping method...")
        
        try:
            # Try to select fastest shipping (usually first option)
            shipping_options = self.driver.find_elements(By.CSS_SELECTOR, "input[name='shipMethod']")
            if shipping_options:
                shipping_options[0].click()
                print("✅ Shipping method selected")
                self._human_delay()
        except Exception as e:
            print(f"⚠️  Shipping selection skipped: {e}")
    
    def place_order(self, verify_only=False):
        """Place the order (or verify without placing if verify_only=True)"""
        print("🎯 Placing order...")
        
        try:
            # Find "Place your order" button
            place_order_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "placeYourOrder1"))
            )
            
            if verify_only:
                print("⚠️  VERIFY ONLY MODE - Not placing order")
                print(f"   Order total visible on page: {self._get_order_total()}")
                return {
                    'success': False,
                    'verify_only': True,
                    'message': 'Order verified but not placed'
                }
            
            # Actually place the order
            self._human_delay(1, 2)
            place_order_btn.click()
            
            # Wait for confirmation
            self._human_delay(5, 8)
            
            # Extract order ID
            order_id = self._extract_order_id()
            
            print(f"✅ Order placed! Amazon Order ID: {order_id}")
            
            return {
                'success': True,
                'amazon_order_id': order_id,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Order placement failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_order_total(self):
        """Extract order total from page"""
        try:
            total_element = self.driver.find_element(By.CSS_SELECTOR, ".grand-total-price")
            return total_element.text
        except:
            return "Unknown"
    
    def _extract_order_id(self):
        """Extract Amazon order ID from confirmation page"""
        try:
            # Wait for order confirmation page
            order_id_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".a-box-group .a-fixed-left-grid-col.a-col-right"))
            )
            order_id = order_id_element.text.strip()
            return order_id
        except:
            # Try alternative method
            try:
                page_source = self.driver.page_source
                import re
                match = re.search(r'Order Number:\s*(\d{3}-\d{7}-\d{7})', page_source)
                if match:
                    return match.group(1)
            except:
                pass
            
            return f"MANUAL-CHECK-{int(time.time())}"
    
    def purchase_product(self, asin, shipping_address, verify_only=False):
        """
        Complete purchase flow: login -> add to cart -> checkout -> place order
        
        Args:
            asin: Amazon product ASIN
            shipping_address: Dict with name, street, city, state, zip
            verify_only: If True, don't actually place order (for testing)
        
        Returns:
            Dict with success status and order details
        """
        result = {
            'success': False,
            'error': None,
            'amazon_order_id': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Setup driver
            self._setup_driver()
            
            # Login
            if not self.login():
                raise Exception("Login failed")
            
            # Add to cart
            if not self.add_to_cart(asin):
                raise Exception("Failed to add product to cart")
            
            # Checkout
            if not self.checkout(shipping_address):
                raise Exception("Checkout failed")
            
            # Place order
            order_result = self.place_order(verify_only=verify_only)
            result.update(order_result)
            
            # Take screenshot for verification
            screenshot_path = f"screenshots/order_{asin}_{int(time.time())}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            result['screenshot'] = screenshot_path
            
            return result
            
        except Exception as e:
            print(f"❌ Purchase failed: {e}")
            result['error'] = str(e)
            
            # Screenshot on error
            try:
                screenshot_path = f"screenshots/error_{int(time.time())}.png"
                os.makedirs("screenshots", exist_ok=True)
                self.driver.save_screenshot(screenshot_path)
                result['screenshot'] = screenshot_path
            except:
                pass
            
            return result
            
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")


def process_order_from_file(order_file, verify_only=False):
    """Process an order from a JSON file"""
    print(f"\n{'='*70}")
    print(f"📦 Processing order: {order_file}")
    print(f"{'='*70}\n")
    
    try:
        # Load order
        with open(order_file, 'r') as f:
            order = json.load(f)
        
        print(f"Product: {order.get('product_name')}")
        print(f"ASIN: {order.get('asin')}")
        print(f"Customer: {order.get('customer_name')}")
        print(f"Amount Paid: ${order.get('amount_paid')}")
        print(f"Your Cost: ${order.get('buy_price')}")
        print(f"Your Profit: ${order.get('profit')}\n")
        
        # Prepare shipping address
        shipping = order.get('shipping_address', {})
        shipping_address = {
            'name': order.get('customer_name'),
            'street': shipping.get('street'),
            'city': shipping.get('city'),
            'state': shipping.get('state'),
            'zip': shipping.get('zip'),
        }
        
        # Create bot and purchase
        bot = AmazonAutoBuyer(headless=False)  # Set to True for background mode
        result = bot.purchase_product(
            asin=order.get('asin'),
            shipping_address=shipping_address,
            verify_only=verify_only
        )
        
        # Update order file with result
        order['bot_result'] = result
        order['status'] = 'ordered' if result['success'] else 'failed'
        order['amazon_order_id'] = result.get('amazon_order_id')
        order['bot_timestamp'] = result['timestamp']
        
        with open(order_file, 'w') as f:
            json.dump(order, f, indent=2)
        
        print(f"\n{'='*70}")
        if result['success']:
            print(f"✅ ORDER SUCCESSFUL")
            print(f"Amazon Order ID: {result.get('amazon_order_id')}")
        else:
            print(f"❌ ORDER FAILED")
            print(f"Error: {result.get('error')}")
        print(f"{'='*70}\n")
        
        return result
        
    except Exception as e:
        print(f"❌ Error processing order: {e}")
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import sys
    
    # Test mode
    if len(sys.argv) > 1:
        order_file = sys.argv[1]
        verify_only = '--verify' in sys.argv
        process_order_from_file(order_file, verify_only=verify_only)
    else:
        print("Usage: python amazon_auto_buyer.py <order_file.json> [--verify]")
        print("\nExample:")
        print("  python amazon_auto_buyer.py orders/ORD-1234567890.json --verify")
        print("\n  Use --verify to test without actually placing the order")
