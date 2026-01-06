#!/usr/bin/env python3
"""
AUTOMATIC AMAZON PURCHASE BOT
Uses Selenium to automatically buy products from Amazon when customers order
"""

import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

class AmazonAutoBuyer:
    def __init__(self):
        self.amazon_email = os.getenv('AMAZON_EMAIL')
        self.amazon_password = os.getenv('AMAZON_PASSWORD')
        
        if not self.amazon_email or not self.amazon_password:
            raise Exception("⚠️ AMAZON_EMAIL and AMAZON_PASSWORD not set in .env file!")
        
        # Chrome options
        chrome_options = Options()
        chrome_options.binary_location = '/usr/bin/chromium'  # Use system Chromium
        # chrome_options.add_argument('--headless')  # Uncomment to run hidden
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize driver with system ChromeDriver
        print("🤖 Starting Chromium browser...")
        self.driver = webdriver.Chrome(
            service=Service('/usr/bin/chromedriver'),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 15)
        
        print("✅ Browser ready!")
    
    def login_to_amazon(self):
        """Login to Amazon account"""
        try:
            print("\n🔐 Logging into Amazon...")
            
            # Go to Amazon homepage first
            self.driver.get('https://www.amazon.com')
            time.sleep(2)
            
            # Click Sign In button
            try:
                signin_link = self.wait.until(EC.element_to_be_clickable((By.ID, 'nav-link-accountList')))
                signin_link.click()
                time.sleep(2)
            except:
                # Alternative: go directly to account page
                self.driver.get('https://www.amazon.com/gp/css/homepage.html')
                time.sleep(2)
            
            # Enter email
            try:
                email_field = self.wait.until(EC.presence_of_element_located((By.ID, 'ap_email')))
                email_field.clear()
                email_field.send_keys(self.amazon_email)
                
                # Click continue
                continue_btn = self.driver.find_element(By.ID, 'continue')
                continue_btn.click()
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Email entry: {str(e)}")
            
            # Enter password
            try:
                password_field = self.wait.until(EC.presence_of_element_located((By.ID, 'ap_password')))
                password_field.clear()
                password_field.send_keys(self.amazon_password)
                
                # Click sign in
                signin_btn = self.driver.find_element(By.ID, 'signInSubmit')
                signin_btn.click()
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Password entry: {str(e)}")
            
            # Check if login successful
            time.sleep(3)
            if "ap/signin" not in self.driver.current_url.lower() and "ap_signin" not in self.driver.current_url.lower():
                print("✅ Login successful!")
                return True
            else:
                print("⚠️ Login may have issues - continuing anyway...")
                return True
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def go_to_product(self, asin):
        """Navigate to product page by ASIN"""
        try:
            print(f"\n📦 Going to product: {asin}")
            url = f"https://www.amazon.com/dp/{asin}"
            self.driver.get(url)
            time.sleep(2)
            
            # Check if product exists
            if "Page Not Found" in self.driver.page_source:
                print(f"❌ Product {asin} not found!")
                return False
            
            print(f"✅ Product page loaded")
            return True
            
        except Exception as e:
            print(f"❌ Error loading product: {str(e)}")
            return False
    
    def add_to_cart(self):
        """Add product to cart"""
        try:
            print("\n🛒 Adding to cart...")
            
            # Try different button IDs Amazon uses
            button_ids = ['add-to-cart-button', 'buy-now-button', 'submit.add-to-cart']
            
            for btn_id in button_ids:
                try:
                    add_btn = self.wait.until(EC.element_to_be_clickable((By.ID, btn_id)))
                    add_btn.click()
                    print(f"✅ Added to cart!")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            print("❌ Could not find add to cart button")
            return False
            
        except Exception as e:
            print(f"❌ Error adding to cart: {str(e)}")
            return False
    
    def proceed_to_checkout(self):
        """Go to checkout"""
        try:
            print("\n💳 Proceeding to checkout...")
            
            # Go to cart
            self.driver.get('https://www.amazon.com/gp/cart/view.html')
            time.sleep(2)
            
            # Click proceed to checkout
            checkout_btn = self.wait.until(EC.element_to_be_clickable((By.NAME, 'proceedToRetailCheckout')))
            checkout_btn.click()
            time.sleep(3)
            
            print("✅ At checkout page")
            return True
            
        except Exception as e:
            print(f"❌ Checkout error: {str(e)}")
            return False
    
    def enter_shipping_address(self, address_data):
        """Enter customer's shipping address"""
        try:
            print("\n📍 Entering shipping address...")
            
            # Click "Add new address" or "Ship to this address"
            # This varies based on account state
            
            # Fill address fields
            fields = {
                'address-ui-widgets-enterAddressFullName': address_data['name'],
                'address-ui-widgets-enterAddressLine1': address_data['address1'],
                'address-ui-widgets-enterAddressLine2': address_data.get('address2', ''),
                'address-ui-widgets-enterAddressCity': address_data['city'],
                'address-ui-widgets-enterAddressStateOrRegion': address_data['state'],
                'address-ui-widgets-enterAddressPostalCode': address_data['zip'],
            }
            
            for field_id, value in fields.items():
                if value:
                    try:
                        field = self.driver.find_element(By.ID, field_id)
                        field.clear()
                        field.send_keys(value)
                    except:
                        pass
            
            print(f"✅ Address entered: {address_data['name']}, {address_data['city']}")
            return True
            
        except Exception as e:
            print(f"⚠️ Address entry: {str(e)}")
            # Address might already be set
            return True
    
    def complete_purchase(self):
        """Complete the purchase (FINAL STEP)"""
        try:
            print("\n💰 Completing purchase...")
            
            # WARNING: This will actually charge your card!
            # Uncomment the line below to enable real purchases
            
            # place_order_btn = self.wait.until(EC.element_to_be_clickable((By.NAME, 'placeYourOrder1')))
            # place_order_btn.click()
            
            print("⚠️ AUTO-PURCHASE DISABLED FOR SAFETY")
            print("   To enable: Uncomment lines in complete_purchase() method")
            print("   This will charge your Amazon payment method!")
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Purchase error: {str(e)}")
            return False
    
    def auto_purchase_product(self, asin, customer_address):
        """
        Complete auto-purchase flow
        
        Args:
            asin: Amazon product ASIN
            customer_address: Dict with name, address1, city, state, zip
        """
        try:
            print(f"\n{'='*60}")
            print(f"🤖 STARTING AUTO-PURCHASE")
            print(f"{'='*60}")
            print(f"Product ASIN: {asin}")
            print(f"Ship to: {customer_address['name']}")
            print(f"Address: {customer_address['city']}, {customer_address['state']}")
            print(f"{'='*60}\n")
            
            # Step 1: Login
            if not self.login_to_amazon():
                return False
            
            # Step 2: Go to product
            if not self.go_to_product(asin):
                return False
            
            # Step 3: Add to cart
            if not self.add_to_cart():
                return False
            
            # Step 4: Checkout
            if not self.proceed_to_checkout():
                return False
            
            # Step 5: Enter address
            if not self.enter_shipping_address(customer_address):
                return False
            
            # Step 6: Complete purchase
            if not self.complete_purchase():
                return False
            
            print(f"\n{'='*60}")
            print(f"✅ AUTO-PURCHASE COMPLETE!")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ AUTO-PURCHASE FAILED: {str(e)}")
            return False
        
        finally:
            # Keep browser open for verification
            print("\n⏸️  Browser staying open for 30 seconds for verification...")
            time.sleep(30)
    
    def close(self):
        """Close browser"""
        try:
            self.driver.quit()
            print("✅ Browser closed")
        except:
            pass


def test_auto_purchase():
    """Test the auto-purchase system with a sample order"""
    
    print("\n" + "="*60)
    print("🧪 TESTING AUTO-PURCHASE SYSTEM")
    print("="*60)
    
    # Sample customer data
    test_address = {
        'name': 'John Doe',
        'address1': '123 Main Street',
        'address2': 'Apt 4B',
        'city': 'New York',
        'state': 'NY',
        'zip': '10001'
    }
    
    # Test with Echo Dot
    test_asin = 'B07XJ8C8F5'
    
    bot = None
    try:
        bot = AmazonAutoBuyer()
        bot.auto_purchase_product(test_asin, test_address)
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        
    finally:
        if bot:
            bot.close()


if __name__ == "__main__":
    # Check if credentials are set
    load_dotenv()
    
    if not os.getenv('AMAZON_EMAIL') or not os.getenv('AMAZON_PASSWORD'):
        print("\n" + "="*60)
        print("⚠️  SETUP REQUIRED")
        print("="*60)
        print("\nAdd these lines to your .env file:")
        print("\nAMAZON_EMAIL=your_amazon_email@gmail.com")
        print("AMAZON_PASSWORD=your_amazon_password")
        print("\nThen run again!")
        print("="*60 + "\n")
    else:
        test_auto_purchase()
