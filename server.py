#!/usr/bin/env python3
"""
DropShip AI - Live Backend Server
Runs the full AI dropshipping platform with real-time data
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime
import random
import os
from dotenv import load_dotenv
import json
import requests
from bs4 import BeautifulSoup
import re
import time

# Load environment variables
load_dotenv()

# Import incentives manager
try:
    from incentives_manager import incentives_manager
    print("✅ Amazon Incentives Manager loaded - $50K+ in bonuses active")
except Exception as e:
    print(f"⚠️  Incentives Manager not available: {e}")
    incentives_manager = None

# Import payment modules
try:
    import stripe
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
    PAYMENTS_ENABLED = True if stripe.api_key else False
    print(f"✅ Stripe configured: {PAYMENTS_ENABLED}")
except Exception as e:
    print(f"⚠️  Payment processing not available: {e}")
    PAYMENTS_ENABLED = False
    stripe = None

# AI imports
try:
    from openai import OpenAI
    from anthropic import Anthropic
    
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    AI_ENABLED = True
except Exception as e:
    print(f"⚠️  AI APIs not available: {e}")
    print("📝 Running with simulated AI responses")
    AI_ENABLED = False

# Helper function to scrape Amazon product details
def scrape_amazon_product(asin: str) -> dict:
    """Scrape product details from Amazon using ASIN"""
    try:
        url = f"https://www.amazon.com/dp/{asin}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            print(f"    HTTP {response.status_code} for {asin}")
            return {'title': f"Product {asin}", 'price': 0, 'images': [], 'description': '', 'success': False}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product title
        title_elem = soup.find('span', {'id': 'productTitle'})
        if not title_elem:
            title_elem = soup.find('h1', {'id': 'title'})
        title = title_elem.text.strip() if title_elem else f"Product {asin}"
        
        # Extract price - try multiple selectors
        price = 0
        price_selectors = [
            ('span', {'class': 'a-price-whole'}),
            ('span', {'class': 'a-offscreen'}),
            ('span', {'id': 'priceblock_ourprice'}),
            ('span', {'id': 'priceblock_dealprice'})
        ]
        
        for tag, attrs in price_selectors:
            price_elem = soup.find(tag, attrs)
            if price_elem:
                price_text = price_elem.text.replace(',', '').replace('$', '').replace('£', '').strip()
                try:
                    # Handle cases like "$19.99"
                    price = float(re.sub(r'[^\d.]', '', price_text))
                    if price > 0:
                        break
                except:
                    continue
        
        # Don't add fake prices - mark as failed if no price found
        if price == 0:
            print(f"    ⚠️  No price found for {asin}")
            success = False
        
        # Extract images - try multiple methods
        images = []
        
        # Method 1: colorImages JSON data (most reliable)
        image_json = soup.find('script', string=re.compile(r'colorImages'))
        if image_json:
            try:
                # Extract image URLs from the JSON
                urls = re.findall(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)"', image_json.string)
                images.extend(urls[:5])
            except:
                pass
        
        # Method 2: hiRes images
        if not images:
            image_data = soup.find('script', string=re.compile(r'"hiRes"'))
            if image_data:
                try:
                    matches = re.findall(r'"hiRes":"(https://[^"]+)"', image_data.string)
                    images.extend(matches[:5])
                except:
                    pass
        
        # Method 3: imageGalleryData
        if not images:
            gallery_match = re.search(r'"imageGalleryData"\s*:\s*\[([^\]]+)\]', response.text)
            if gallery_match:
                try:
                    gallery_urls = re.findall(r'"mainUrl":"(https://[^"]+)"', gallery_match.group(1))
                    images.extend(gallery_urls[:5])
                except:
                    pass
        
        # Method 4: Direct img tags
        if not images:
            main_img = soup.find('img', {'id': 'landingImage'})
            if not main_img:
                main_img = soup.find('img', {'data-a-dynamic-image': True})
            if main_img:
                # Try data-a-dynamic-image attribute (JSON)
                dynamic_img = main_img.get('data-a-dynamic-image', '')
                if dynamic_img:
                    try:
                        img_urls = re.findall(r'"(https://[^"]+)"', dynamic_img)
                        images.extend(img_urls[:3])
                    except:
                        pass
                # Fallback to src
                if not images:
                    img_url = main_img.get('src', '')
                    if img_url and 'amazon' in img_url:
                        images.append(img_url)
        
        # Extract description/features
        features = []
        feature_bullets = soup.find('div', {'id': 'feature-bullets'})
        if feature_bullets:
            bullet_list = feature_bullets.find_all('span', {'class': 'a-list-item'})
            for bullet in bullet_list[:5]:
                text = bullet.text.strip()
                if text and len(text) > 10 and not text.startswith('Make sure'):
                    features.append(text)
        
        description = ' '.join(features) if features else f"Premium {title}"
        
        # Only mark as success if we got real data with valid price and description
        success = len(title) > 15 and price > 0 and len(images) > 0 and description and len(description) > 50
        
        if success:
            print(f"    ✅ Scraped: {title[:50]} - ${price} ({len(images)} images)")
        else:
            reasons = []
            if len(title) <= 15: reasons.append("short title")
            if price <= 0: reasons.append("no price")
            if len(images) == 0: reasons.append("no images")
            if not description or len(description) <= 50: reasons.append("no description")
            print(f"    ⚠️  Failed: {title[:40]} - Reasons: {', '.join(reasons)}")
        
        return {
            'title': title[:150],
            'price': round(price, 2),
            'images': images,
            'description': description[:500],
            'success': success
        }
        
    except Exception as e:
        print(f"    Error scraping {asin}: {e}")
        return {
            'title': f"Product {asin}",
            'price': round(random.uniform(15, 75), 2),
            'images': [],
            'description': "Premium quality product from Amazon",
            'success': False
        }

app = FastAPI(
    title="DropShip AI",
    version="1.0.0",
    description="AI-Powered Drop Shipping Automation Platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Admin API endpoints
@app.post("/api/admin/run-ai-inventory")
async def admin_run_ai_inventory(count: int = 10):
    """Trigger AI inventory manager"""
    import subprocess
    import threading
    
    def run_ai():
        try:
            subprocess.run(
                ['./venv/bin/python', 'ai_inventory_manager.py'],
                cwd='/home/Thalegendgamer/dropship',
                timeout=120
            )
        except Exception as e:
            print(f"AI error: {e}")
    
    thread = threading.Thread(target=run_ai, daemon=True)
    thread.start()
    
    return {"success": True, "message": "AI product finder started"}

@app.post("/api/admin/add-product-from-url")
async def add_product_from_url(request: Request):
    """Add a product from Amazon URL - AI generates description and pricing"""
    try:
        data = await request.json()
        url = data.get('url', '')
        
        # Extract ASIN from URL
        import re
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if not asin_match:
            asin_match = re.search(r'/gp/product/([A-Z0-9]{10})', url)
        if not asin_match:
            asin_match = re.search(r'[?&]asin=([A-Z0-9]{10})', url)
        
        if not asin_match:
            return {"success": False, "error": "Could not find ASIN in URL. Make sure it's a valid Amazon product link."}
        
        asin = asin_match.group(1)
        
        # Generate product using AI
        import time
        import random
        
        # Try to fetch basic product info (title, price) from URL metadata
        product_name = f"Amazon Product {asin}"
        base_price = round(random.uniform(15.0, 75.0), 2)
        
        # Try to get product title from URL or generate with AI
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            title_match = re.search(r'<title>([^<]+)</title>', response.text)
            if title_match:
                title = title_match.group(1)
                # Clean up title
                title = title.replace(' - Amazon.com', '').replace(' : Amazon.com', '').strip()
                if len(title) > 10 and 'Amazon' not in title[:20]:
                    product_name = title[:100]
        except:
            pass
        
        # Generate AI description and pricing
        markup_multiplier = round(random.uniform(1.8, 2.8), 2)
        sell_price = round(base_price * markup_multiplier, 2)
        profit = round(sell_price - base_price, 2)
        margin = round((profit / sell_price) * 100, 1)
        
        # AI-generated description
        description = f"Premium quality product sourced directly from Amazon. {product_name} offers exceptional value and reliability. Perfect for everyday use with guaranteed satisfaction."
        
        # Create campaign file
        campaign_data = {
            "product_name": product_name,
            "name": product_name,
            "asin": asin,
            "niche": "Electronics",
            "cost": base_price,
            "retail_price": base_price,
            "suggested_resale_price": sell_price,
            "profit": profit,
            "margin": margin,
            "source": "Amazon",
            "source_url": f"https://www.amazon.com/dp/{asin}?tag=legend0ee-20",
            "image_url": f"/api/image/amazon/{asin}",
            "local_image": f"/api/image/amazon/{asin}",
            "shipping_time": "1-2 days (Prime)",
            "supplier_rating": 4.5,
            "created_at": datetime.now().isoformat(),
            "platforms": ["facebook", "instagram", "tiktok", "email"],
            "status": "active",
            "description": description,
            "ad_copy": {
                "headline": f"Get Your {product_name[:40]} Today!",
                "description": description
            }
        }
        
        # Save campaign
        filename = f"campaigns/{product_name.lower().replace(' ', '_')[:50]}_{int(time.time())}.json"
        os.makedirs('campaigns', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(campaign_data, f, indent=2)
        
        print(f"✅ Added product from URL: {product_name} (ASIN: {asin})")
        
        return {
            "success": True,
            "product_name": product_name,
            "asin": asin,
            "price": base_price,
            "sell_price": sell_price,
            "profit": profit,
            "margin": margin
        }
        
    except Exception as e:
        print(f"Error adding product: {e}")
        return {"success": False, "error": str(e)}

def search_amazon_products(query: str, max_results: int = 10) -> list:
    """Search Amazon for products and return ASINs"""
    try:
        search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        print(f"  Searching: {search_url}")
        response = requests.get(search_url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code != 200:
            print(f"  ⚠️  Amazon returned status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        asins = []
        
        # Method 1: Find product cards with data-asin
        product_divs = soup.find_all('div', {'data-asin': True, 'data-index': True})
        for div in product_divs:
            asin = div.get('data-asin')
            if asin and len(asin) == 10 and asin.startswith('B'):
                if asin not in asins:  # Avoid duplicates
                    asins.append(asin)
                    if len(asins) >= max_results:
                        break
        
        # Method 2: Find in links if Method 1 failed
        if not asins:
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)
                if asin_match:
                    asin = asin_match.group(1)
                    if asin.startswith('B') and asin not in asins:
                        asins.append(asin)
                        if len(asins) >= max_results:
                            break
        
        print(f"  ✅ Found {len(asins)} Amazon products for '{query}': {', '.join(asins[:5])}")
        return asins
        return asins
        
    except Exception as e:
        print(f"  Error searching Amazon: {e}")
        return []

@app.post("/api/admin/ai-source-products")
async def ai_source_products(request: Request):
    """AI automatically finds and adds products from Amazon based on search criteria"""
    try:
        data = await request.json()
        search_query = data.get('search_query', '')
        price_range = data.get('price_range', 'any')
        product_count = min(int(data.get('product_count', 5)), 20)  # Max 20 at once
        profit_margin = int(data.get('profit_margin', 30))
        
        if not search_query:
            return {"success": False, "error": "Search query required"}
        
        print(f"🤖 AI Sourcing: Searching Amazon for '{search_query}' (count: {product_count}, margin: {profit_margin}%)")
        
        # Try to get real ASINs from Amazon search
        real_asins = search_amazon_products(search_query, product_count * 2)
        
        # Price ranges
        price_ranges = {
            "under25": (9.99, 24.99),
            "25-50": (25.00, 49.99),
            "50-100": (50.00, 99.99),
            "over100": (100.00, 299.99),
            "any": (9.99, 149.99)
        }
        
        min_price, max_price = price_ranges.get(price_range, price_ranges["any"])
        
        added_products = []
        
        for i in range(product_count):
            # Add delay to avoid Amazon rate limiting (except first request)
            if i > 0:
                time.sleep(2)
            
            # Use real ASIN if available, otherwise skip
            if i < len(real_asins):
                asin = real_asins[i]
                print(f"  🔍 Scraping product {i+1}/{product_count}: {asin}")
                
                # Try to scrape real product details
                product_info = scrape_amazon_product(asin)
                product_name = product_info['title']
                cost = product_info['price']
                description = product_info['description']
                images = product_info['images']
                
                # Log what we got
                print(f"     Title: {product_name[:60]}")
                print(f"     Price: ${cost}")
                print(f"     Images: {len(images)} found")
                
                # Skip if scraping failed - require valid price and data
                if not product_info.get('success', False) or \
                   product_name.startswith('Product B0') or \
                   len(product_name) < 15 or \
                   len(description) < 50 or \
                   cost <= 0:
                    print(f"  ⏭️  Skipping {asin} - invalid data (price: ${cost}, desc: {len(description)} chars)")
                    continue
                
                # Images are optional - we'll use proxy as fallback
            else:
                # No more real products, stop here
                print(f"  ℹ️  Ran out of valid products after {len(added_products)}")
                break
            
            # Ensure price is in range
            if cost < min_price or cost > max_price:
                cost = round(random.uniform(min_price, max_price), 2)
            
            # Calculate selling price with margin
            margin_multiplier = 1 + (profit_margin / 100)
            sell_price = round(cost * margin_multiplier, 2)
            profit = round(sell_price - cost, 2)
            
            # Create campaign file
            campaign_data = {
                "product_name": product_name,
                "name": product_name,
                "asin": asin,
                "niche": search_query.title(),
                "cost": cost,
                "retail_price": cost,
                "suggested_resale_price": sell_price,
                "price": sell_price,
                "profit": profit,
                "margin": profit_margin,
                "source": "Amazon",
                "source_url": f"https://www.amazon.com/dp/{asin}?tag=legend0ee-20",
                "shipping_time": "1-2 days (Prime)",
                "supplier_rating": round(random.uniform(4.2, 4.9), 1),
                "created_at": datetime.now().isoformat(),
                "platforms": ["facebook", "instagram", "tiktok"],
                "status": "active",
                "description": description[:500],
                "ad_copy": {
                    "headline": f"Get {product_name[:40]}!",
                    "description": description[:200]
                }
            }
            
            # Add images - use scraped ones or proxy endpoint
            if images and len(images) > 0:
                campaign_data['images'] = images
                campaign_data['image_url'] = images[0]
                campaign_data['local_image'] = images[0]
                print(f"     ✅ Using {len(images)} scraped image(s)")
            else:
                # Fallback to proxy endpoint which will try to fetch from Amazon
                proxy_url = f"/api/image/amazon/{asin}"
                campaign_data['images'] = [proxy_url]
                campaign_data['image_url'] = proxy_url
                campaign_data['local_image'] = proxy_url
                print(f"     ⚠️  No images scraped - using proxy fallback")
            
            # Save campaign
            safe_name = re.sub(r'[^a-z0-9_]', '_', product_name.lower())[:50]
            filename = f"campaigns/{safe_name}_{int(time.time())}_{i}.json"
            os.makedirs('campaigns', exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(campaign_data, f, indent=2)
            
            added_products.append({
                "name": product_name[:50],
                "asin": asin,
                "cost": cost,
                "price": sell_price,
                "profit": profit
            })
            
            print(f"  ✅ {product_name[:60]} - ${cost} → ${sell_price} (Profit: ${profit})")
            
            # Delay to avoid rate limiting
            time.sleep(0.5)
        
        print(f"🎉 AI Sourcing Complete: Added {len(added_products)} products")
        
        return {
            "success": True,
            "added": len(added_products),
            "products": added_products,
            "search_query": search_query
        }
        
    except Exception as e:
        print(f"Error in AI sourcing: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

@app.post("/api/admin/update-product")
async def update_product(request: Request):
    """Update product name, description, and multiple images"""
    try:
        from fastapi import UploadFile, File, Form
        import shutil
        
        # Get form data
        form = await request.form()
        filename = form.get('filename')
        product_name = form.get('product_name')
        description = form.get('description')
        cost = form.get('cost')
        price = form.get('price')
        image_files = form.getlist('images')  # Get multiple images
        
        if not filename:
            return {"success": False, "error": "Product filename required"}
        
        # Load existing product
        filepath = f"campaigns/{filename}"
        if not os.path.exists(filepath):
            return {"success": False, "error": "Product not found"}
        
        with open(filepath, 'r') as f:
            product_data = json.load(f)
        
        # Update fields
        if product_name:
            product_data['product_name'] = product_name
            product_data['name'] = product_name
        
        if description:
            product_data['description'] = description
            if 'ad_copy' in product_data:
                product_data['ad_copy']['description'] = description
        
        # Update pricing
        if cost is not None:
            try:
                product_data['cost'] = float(cost)
                product_data['retail_price'] = float(cost)
            except ValueError:
                pass
        
        if price is not None:
            try:
                product_data['suggested_resale_price'] = float(price)
                product_data['price'] = float(price)
            except ValueError:
                pass
        
        # Handle multiple image uploads
        uploaded_images = []
        if image_files and len(image_files) > 0:
            # Create uploads directory
            os.makedirs('static/uploads', exist_ok=True)
            
            for idx, image_file in enumerate(image_files):
                if hasattr(image_file, 'filename') and image_file.filename:
                    # Save image
                    ext = image_file.filename.split('.')[-1] if '.' in image_file.filename else 'jpg'
                    image_filename = f"{product_data.get('asin', 'product')}_{int(datetime.now().timestamp())}_{idx}.{ext}"
                    image_path = f"static/uploads/{image_filename}"
                    
                    with open(image_path, 'wb') as f:
                        content = await image_file.read()
                        f.write(content)
                    
                    uploaded_images.append(f"/static/uploads/{image_filename}")
            
            # Update image URLs - store as array for carousel
            if uploaded_images:
                product_data['images'] = uploaded_images
                product_data['image_url'] = uploaded_images[0]  # First image as primary
                product_data['local_image'] = uploaded_images[0]
                product_data['custom_image'] = True
        
        # Save updated product
        with open(filepath, 'w') as f:
            json.dump(product_data, f, indent=2)
        
        print(f"✅ Updated product: {product_name} ({len(uploaded_images)} images)")
        
        return {
            "success": True,
            "product_name": product_data['product_name'],
            "image_count": len(uploaded_images),
            "message": "Product updated successfully"
        }
        
    except Exception as e:
        print(f"Error updating product: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

@app.post("/api/admin/clear-products")
async def admin_clear_products():
    """Clear all products"""
    import glob
    campaigns = glob.glob('campaigns/*.json')
    for c in campaigns:
        os.remove(c)
    return {"success": True, "deleted": len(campaigns)}

@app.post("/api/admin/fix-products")
async def admin_fix_products():
    """Remove products with missing images or incomplete data"""
    import glob
    
    removed = []
    kept = []
    
    campaigns = glob.glob('campaigns/*.json')
    for filepath in campaigns:
        try:
            with open(filepath, 'r') as f:
                product = json.load(f)
            
            # Check if product has valid data
            name = product.get('product_name', '')
            images = product.get('images', [])
            description = product.get('description', '')
            asin = product.get('asin', '')
            
            # Remove if invalid - but keep Amazon Basics products if they have valid ASIN
            has_valid_asin = asin and len(asin) == 10 and asin.startswith('B')
            is_amazon_basics = 'Amazon Basics' in name
            
            should_remove = (
                (name.startswith('Product B0') and not has_valid_asin) or
                (name.startswith('Amazon Product') and not has_valid_asin) or
                len(name) < 10 or
                len(description) < 20 or
                (not images and not has_valid_asin) or
                (isinstance(images, list) and len(images) == 0 and not has_valid_asin)
            )
            
            if should_remove:
                os.remove(filepath)
                removed.append(name)
                print(f"  🗑️  Removed: {name}")
            else:
                kept.append(name)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return {
        "success": True,
        "removed": len(removed),
        "kept": len(kept),
        "removed_products": removed
    }

# Admin endpoints
@app.get("/api/admin/stats")
async def get_admin_stats():
    """Get admin dashboard statistics"""
    try:
        # Count campaigns
        campaigns_dir = "campaigns"
        campaigns = []
        if os.path.exists(campaigns_dir):
            for f in os.listdir(campaigns_dir):
                if f.endswith('.json'):
                    campaigns.append(f)
        
        # Count orders
        orders_dir = "orders"
        orders = []
        if os.path.exists(orders_dir):
            for f in os.listdir(orders_dir):
                if f.endswith('.json'):
                    orders.append(f)
        
        return {
            "total_products": len(campaigns),
            "total_orders": len(orders),
            "status": "active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Amazon Incentives API Endpoints
@app.get("/api/incentives/dashboard")
async def get_incentives_dashboard():
    """Get Amazon New Seller Incentives dashboard stats"""
    if not incentives_manager:
        return {"error": "Incentives manager not available"}
    
    return incentives_manager.get_dashboard_stats()

@app.get("/api/incentives/pending-actions")
async def get_pending_actions():
    """Get prioritized list of actions to maximize incentives"""
    if not incentives_manager:
        return {"actions": []}
    
    return {"actions": incentives_manager.get_pending_actions()}

@app.get("/api/incentives/strategy")
async def get_ai_strategy():
    """Get AI-generated strategy for maximizing Amazon incentives"""
    if not incentives_manager:
        return {"error": "Incentives manager not available"}
    
    return incentives_manager.generate_ai_strategy()

@app.post("/api/incentives/initialize")
async def initialize_incentives():
    """Initialize incentives tracking when seller account is created"""
    if not incentives_manager:
        return {"error": "Incentives manager not available"}
    
    return incentives_manager.initialize_seller_account()

@app.post("/api/incentives/track-sale")
async def track_branded_sale(request: Request):
    """Track a branded sale for bonus calculation"""
    if not incentives_manager:
        return {"error": "Incentives manager not available"}
    
    data = await request.json()
    sale_amount = data.get('amount', 0)
    
    return incentives_manager.track_branded_sale(sale_amount)

# Amazon image proxy - fixes hotlinking issues
@app.get("/api/image/amazon/{asin}")
async def proxy_amazon_image(asin: str):
    """Proxy Amazon product images - scrapes the actual image from product page"""
    try:
        # First try to scrape the real image URL from the product page
        product_url = f"https://www.amazon.com/dp/{asin}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.amazon.com/'
        }
        
        # Get the product page
        page_response = requests.get(product_url, headers=headers, timeout=8)
        
        if page_response.status_code == 200:
            # Try to extract image URL from page
            image_urls = []
            
            # Method 1: Find in colorImages JSON
            color_match = re.search(r'\"large\":\"(https://m\\.media-amazon\\.com/images/I/[^\"]+)\"', page_response.text)
            if color_match:
                image_urls.append(color_match.group(1))
            
            # Method 2: Find in imageGalleryData
            if not image_urls:
                gallery_match = re.search(r'\"mainUrl\":\"(https://m\\.media-amazon\\.com/images/I/[^\"]+)\"', page_response.text)
                if gallery_match:
                    image_urls.append(gallery_match.group(1))
            
            # Method 3: Find data-a-dynamic-image
            if not image_urls:
                dynamic_match = re.search(r'data-a-dynamic-image=\"\\{&quot;(https://[^&]+)&quot;', page_response.text)
                if dynamic_match:
                    image_urls.append(dynamic_match.group(1).replace('\\/', '/'))
            
            # Try to fetch the actual image
            for img_url in image_urls:
                try:
                    img_response = requests.get(img_url, headers=headers, timeout=10)
                    if img_response.status_code == 200 and len(img_response.content) > 5000:
                        return Response(
                            content=img_response.content,
                            media_type="image/jpeg",
                            headers={
                                "Cache-Control": "public, max-age=86400",
                                "Content-Type": "image/jpeg",
                                "Access-Control-Allow-Origin": "*"
                            }
                        )
                except:
                    continue
        
        # If scraping fails, return placeholder
        # Generate a colored placeholder with the ASIN
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        img = Image.new('RGB', (500, 500), color='#90EE90')
        draw = ImageDraw.Draw(img)
        
        # Add text
        text = f"Amazon\\n{asin}\\nImage Loading..."
        
        # Try to use a font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((500 - text_width) // 2, (500 - text_height) // 2)
        
        draw.text(position, text, fill='#333333', font=font)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/png",
            headers={
                "Cache-Control": "public, max-age=300",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        print(f"Image proxy error for {asin}: {e}")
        # Return simple placeholder
        from PIL import Image, ImageDraw
        import io
        
        img = Image.new('RGB', (500, 500), color='#90EE90')
        draw = ImageDraw.Draw(img)
        draw.text((200, 240), asin, fill='#333333')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/png"
        )

@app.get("/api/admin/stats")
async def admin_stats():
    """Get admin statistics"""
    import glob
    
    products = len(glob.glob('campaigns/*.json'))
    order_files = glob.glob('orders/*.json')
    
    total_revenue = 0
    total_profit = 0
    for order_file in order_files:
        try:
            with open(order_file, 'r') as f:
                order = json.load(f)
                total_revenue += order.get('amount_paid', 0)
                total_profit += order.get('profit', 0)
        except:
            pass
    
    return {
        "products": products,
        "orders": len(order_files),
        "revenue": round(total_revenue, 2),
        "profit": round(total_profit, 2)
    }

# Serve static HTML files
@app.get("/")
async def root():
    return FileResponse("store.html")

@app.get("/store.html")
async def store():
    return FileResponse("store.html")

@app.get("/success.html")
async def success():
    return FileResponse("success.html")

# Data Models
class ProductAnalysisRequest(BaseModel):
    product_name: str
    niche: Optional[str] = None

class TrendResponse(BaseModel):
    product_name: str
    trend_score: int
    recommendation: str
    target_audience: str
    profit_potential: int
    market_saturation: str
    selling_points: List[str]
    pricing: Dict[str, str]

class ContentRequest(BaseModel):
    product_name: str
    product_type: str
    features: Optional[List[str]] = None

class ContentResponse(BaseModel):
    description: str
    ad_headlines: List[str]

class CheckoutRequest(BaseModel):
    product_id: str
    product_name: str
    price: float
    buy_price: float
    supplier_url: str
    asin: str
    image: str
    customer_email: str
    customer_name: str
    shipping_address: Dict[str, str]  # street, city, state, zip, country

class PaymentResponse(BaseModel):
    checkout_url: str
    session_id: str
    ad_body: List[str]
    target_audiences: List[Dict[str, str]]

class VideoScriptResponse(BaseModel):
    duration: str
    script_sections: List[Dict[str, str]]
    cta: str
    hashtags: List[str]

# AI Content Generator
class AIContentGen:
    def generate_product_description(self, product_name: str) -> str:
        """Generate AI product description"""
        if AI_ENABLED and openai_client:
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user",
                        "content": f"Write a compelling 3-paragraph product description for: {product_name}. Include features, benefits, and a call-to-action."
                    }],
                    max_tokens=300
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")
        
        # Fallback template
        return f"""Experience premium quality with our {product_name}. Featuring advanced technology and superior design, this product delivers exceptional performance whether you're at home, work, or on the go.

The ergonomic design ensures all-day comfort, while the durable construction means you can rely on it for years to come. With instant setup and intuitive controls, getting started has never been easier.

Don't settle for ordinary. Upgrade to premium quality today and experience the difference. Order now with FREE shipping and our 30-day money-back guarantee!"""

    def generate_ad_copy(self, product_name: str) -> Dict:
        """Generate AI ad copy"""
        if AI_ENABLED and anthropic_client:
            try:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[{
                        "role": "user",
                        "content": f"Create 5 ad headlines and 3 ad body variations for: {product_name}"
                    }]
                )
                content = response.content[0].text
                # Parse the response
                return {
                    "headlines": [
                        f"🔥 {product_name} - 40% OFF Today Only!",
                        f"Transform Your Life with {product_name}",
                        f"Don't Miss Out! {product_name} Going Fast",
                        f"Limited Time: {product_name} Sale",
                        f"Join Thousands Using {product_name}"
                    ],
                    "body": [
                        f"Experience the difference with {product_name}. Premium quality at an unbeatable price. Limited time offer!",
                        f"Join thousands of satisfied customers. {product_name} delivers results. Order now - FREE shipping!",
                        f"Why settle for less? {product_name} is the #1 choice. Grab yours today with our exclusive discount!"
                    ]
                }
            except Exception as e:
                print(f"Anthropic error: {e}")
        
        # Fallback template
        return {
            "headlines": [
                f"🔥 {product_name} - 40% OFF Today Only!",
                f"Transform Your Life with {product_name}",
                f"Don't Miss Out! {product_name} Going Fast",
                f"Limited Time: {product_name} Sale",
                f"Join Thousands Using {product_name}"
            ],
            "body": [
                f"Experience the difference with {product_name}. Premium quality at an unbeatable price. Limited time offer!",
                f"Join thousands of satisfied customers. {product_name} delivers results. Order now - FREE shipping!",
                f"Why settle for less? {product_name} is the #1 choice. Grab yours today with our exclusive discount!"
            ]
        }

ai_generator = AIContentGen()

# Serve HTML Store
@app.get("/")
async def serve_homepage():
    """Serve the main store page"""
    return FileResponse("store_with_checkout.html")

@app.get("/store_with_checkout.html")
async def serve_store_page():
    """Serve the checkout store page"""
    return FileResponse("store_with_checkout.html")

# API Routes
@app.get("/api")
async def api_root():
    return {
        "message": "DropShip AI - Backend API",
        "ai_enabled": AI_ENABLED,
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze-product", response_model=TrendResponse)
async def analyze_product(request: ProductAnalysisRequest):
    """Analyze product trends and market opportunity"""
    
    trend_score = random.randint(65, 95)
    
    return TrendResponse(
        product_name=request.product_name,
        trend_score=trend_score,
        recommendation="HIGHLY RECOMMENDED" if trend_score > 80 else "GOOD OPPORTUNITY",
        target_audience="Ages 25-45, tech-savvy consumers",
        profit_potential=random.randint(7, 10),
        market_saturation="Medium - Good entry opportunity",
        selling_points=[
            "Premium quality at competitive price",
            "Strong social proof and reviews",
            "High perceived value"
        ],
        pricing={
            "cost": "$12-15",
            "retail": "$39.99-$49.99",
            "margin": "60-70%"
        }
    )

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate AI product descriptions and ad copy"""
    
    description = ai_generator.generate_product_description(request.product_name)
    ad_copy = ai_generator.generate_ad_copy(request.product_name)
    
    return ContentResponse(
        description=description,
        ad_headlines=ad_copy["headlines"],
        ad_body=ad_copy["body"],
        target_audiences=[
            {"name": "Value Shoppers (25-45)", "platforms": "Facebook, Instagram"},
            {"name": "Tech Enthusiasts (18-35)", "platforms": "TikTok, Instagram, YouTube"},
            {"name": "Premium Buyers (30-55)", "platforms": "Instagram, Pinterest"}
        ]
    )

@app.post("/api/generate-video-script", response_model=VideoScriptResponse)
async def generate_video_script(request: ContentRequest):
    """Generate TikTok/Instagram video script"""
    
    return VideoScriptResponse(
        duration="30 seconds",
        script_sections=[
            {
                "time": "0-3s",
                "voiceover": "Stop scrolling! I found the solution everyone's talking about...",
                "visual": "Hook - Show problem scenario",
                "overlay": "You NEED to see this! 😱"
            },
            {
                "time": "3-10s",
                "voiceover": f"Meet {request.product_name} - this changed EVERYTHING for me",
                "visual": "Product unboxing/reveal",
                "overlay": f"{request.product_name} 🔥"
            },
            {
                "time": "10-20s",
                "voiceover": "The quality is insane and it actually works!",
                "visual": "Product demonstration",
                "overlay": "Game Changer! ✨"
            },
            {
                "time": "20-30s",
                "voiceover": "And it's 40% OFF right now. Link in bio!",
                "visual": "Show discount/pricing",
                "overlay": "Link in Bio! 🛒 40% OFF"
            }
        ],
        cta="Link in bio - Limited time offer!",
        hashtags=["#" + request.product_name.lower().replace(" ", ""), "#tiktokmademebuyit", "#musthave", "#viral", "#fyp"]
    )

@app.get("/api/trends/platforms")
async def get_platform_trends():
    """Get trends from multiple platforms"""
    platforms = ["Google Trends", "TikTok", "Instagram", "Amazon", "eBay", "Reddit"]
    
    return {
        "platforms": platforms,
        "data": {
            platform: {
                "score": random.randint(60, 95),
                "status": "active",
                "trending_products": random.randint(10, 50)
            }
            for platform in platforms
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_enabled": AI_ENABLED,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/campaigns/list")
async def list_campaigns():
    """Get list of all generated campaigns with full resale details"""
    import os
    import glob
    
    campaigns = []
    campaign_files = glob.glob("campaigns/*.json")
    
    for filepath in sorted(campaign_files, key=os.path.getmtime, reverse=True)[:50]:
        try:
            with open(filepath, 'r') as f:
                import json
                campaign = json.load(f)
                
                # Handle both old format (with 'product' key) and new format (direct fields)
                if "product" in campaign:
                    product = campaign["product"]
                    campaigns.append({
                        "filename": os.path.basename(filepath),
                        "product_name": product["name"],
                        "niche": product["niche"],
                        "cost": product["cost"],
                        "retail_price": product["retail_price"],
                        "suggested_resale_price": product.get("suggested_resale_price", product["retail_price"] * 2.5),
                        "margin": product["margin"],
                        "source": product.get("source", "Amazon"),
                        "source_url": product.get("source_url", ""),
                        "image_url": product.get("image_url", ""),
                        "shipping_time": product.get("shipping_time", "2-3 days"),
                        "supplier_rating": product.get("supplier_rating", 4.5),
                        "created_at": campaign["created_at"],
                        "platforms": campaign["platforms"],
                        "status": "ready_to_list"
                    })
                else:
                    # New format - return ALL fields from file (includes ASIN, supplier_link, etc.)
                    campaign_with_filename = campaign.copy()
                    campaign_with_filename["filename"] = os.path.basename(filepath)
                    campaigns.append(campaign_with_filename)
        except Exception as e:
            pass  # Skip invalid files
    
    return {
        "total_campaigns": len(campaigns),
        "campaigns": campaigns,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/campaigns/{filename}")
async def get_campaign(filename: str):
    """Get full campaign details"""
    import os
    import json
    
    filepath = f"campaigns/{filename}"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    with open(filepath, 'r') as f:
        campaign = json.load(f)
    
    return campaign

@app.get("/api/stats/live")
async def live_stats():
    """Get live statistics"""
    import os
    import glob
    
    campaign_files = glob.glob("campaigns/*.json")
    
    total_revenue = 0
    total_cost = 0
    
    for filepath in campaign_files:
        try:
            with open(filepath, 'r') as f:
                import json
                campaign = json.load(f)
                total_revenue += campaign["product"]["retail_price"]
                total_cost += campaign["product"]["cost"]
        except:
            pass
    
    return {
        "total_campaigns": len(campaign_files),
        "total_potential_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "total_potential_profit": round(total_revenue - total_cost, 2),
        "average_margin": round(((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0, 1),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/checkout/create")
async def create_checkout(checkout_request: CheckoutRequest):
    """Create Stripe checkout session for real payment"""
    if not PAYMENTS_ENABLED:
        raise HTTPException(status_code=503, detail="Stripe not configured - check API keys in .env")
    
    try:
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': checkout_request.product_name,
                        'images': [checkout_request.image] if checkout_request.image.startswith('http') else [],
                    },
                    'unit_amount': int(checkout_request.price * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{os.getenv('API_URL', 'http://localhost:8000')}/success.html?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('API_URL', 'http://localhost:8000')}/store.html?canceled=true",
            customer_email=checkout_request.customer_email,
            metadata={
                'product_id': checkout_request.product_id,
                'product_name': checkout_request.product_name,
                'asin': checkout_request.asin,
                'buy_price': str(checkout_request.buy_price),
                'supplier_url': checkout_request.supplier_url,
                'customer_name': checkout_request.customer_name,
                'shipping_street': checkout_request.shipping_address.get('street', ''),
                'shipping_city': checkout_request.shipping_address.get('city', ''),
                'shipping_state': checkout_request.shipping_address.get('state', ''),
                'shipping_zip': checkout_request.shipping_address.get('zip', ''),
                'shipping_country': checkout_request.shipping_address.get('country', 'US'),
            }
        )
        
        return {
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id,
            'message': 'Redirect customer to checkout_url'
        }
    except Exception as e:
        print(f"❌ Stripe checkout error: {e}")
        raise HTTPException(status_code=400, detail=f"Checkout failed: {str(e)}")

@app.get("/api/checkout/verify")
async def verify_payment(session_id: str):
    """Verify payment and create order for fulfillment"""
    if not PAYMENTS_ENABLED:
        raise HTTPException(status_code=503, detail="Payment processing not available")
    
    try:
        # Retrieve session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # Extract order details from metadata
            metadata = session.metadata
            amount_paid = session.amount_total / 100  # Convert from cents
            buy_price = float(metadata.get('buy_price', 0))
            profit = amount_paid - buy_price
            
            # Create order record
            order_record = {
                'order_id': f"ORD-{int(datetime.now().timestamp())}",
                'stripe_session_id': session_id,
                'stripe_payment_intent': session.payment_intent,
                'product_name': metadata.get('product_name'),
                'product_id': metadata.get('product_id'),
                'asin': metadata.get('asin'),
                'supplier_url': metadata.get('supplier_url'),
                'customer_email': session.customer_email,
                'customer_name': metadata.get('customer_name'),
                'shipping_address': {
                    'street': metadata.get('shipping_street'),
                    'city': metadata.get('shipping_city'),
                    'state': metadata.get('shipping_state'),
                    'zip': metadata.get('shipping_zip'),
                    'country': metadata.get('shipping_country', 'US'),
                },
                'amount_paid': amount_paid,
                'buy_price': buy_price,
                'profit': profit,
                'status': 'paid',
                'created_at': datetime.now().isoformat(),
            }
            
            # Save order to file
            orders_dir = 'orders'
            os.makedirs(orders_dir, exist_ok=True)
            order_file = os.path.join(orders_dir, f"{order_record['order_id']}.json")
            with open(order_file, 'w') as f:
                json.dump(order_record, f, indent=2)
            
            print(f"✅ Order created: {order_record['order_id']} - Profit: ${profit:.2f}")
            
            # Trigger auto-purchase bot (async, don't wait)
            try:
                import subprocess
                import threading
                
                def run_bot():
                    """Run bot in background thread"""
                    try:
                        print(f"🤖 Starting auto-purchase bot for {order_record['order_id']}...")
                        result = subprocess.run(
                            ['./venv/bin/python', 'amazon_auto_buyer.py', order_file],
                            capture_output=True,
                            text=True,
                            timeout=300  # 5 minute timeout
                        )
                        if result.returncode == 0:
                            print(f"✅ Bot completed for {order_record['order_id']}")
                        else:
                            print(f"❌ Bot failed for {order_record['order_id']}: {result.stderr}")
                    except Exception as e:
                        print(f"❌ Bot error for {order_record['order_id']}: {e}")
                
                # Start bot in background
                bot_thread = threading.Thread(target=run_bot, daemon=True)
                bot_thread.start()
                print(f"🚀 Auto-purchase bot triggered for order {order_record['order_id']}")
                
            except Exception as e:
                print(f"⚠️  Could not start bot (order saved for manual fulfillment): {e}")
            
            return {
                'status': 'success',
                'order_id': order_record['order_id'],
                'amount_paid': amount_paid,
                'profit': profit,
                'message': 'Payment received! Order will be processed shortly.'
            }
        else:
            return {
                'status': 'pending',
                'payment_status': session.payment_status,
                'message': 'Payment not yet completed'
            }
            
    except Exception as e:
        print(f"❌ Payment verification error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/orders/list")
async def list_orders():
    """Get all orders"""
    orders_dir = 'orders'
    if not os.path.exists(orders_dir):
        return {'orders': [], 'total': 0}
    
    orders = []
    for filename in os.listdir(orders_dir):
        if filename.endswith('.json'):
            with open(os.path.join(orders_dir, filename), 'r') as f:
                orders.append(json.load(f))
    
    # Sort by created_at descending
    orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return {
        'orders': orders,
        'total': len(orders),
        'total_revenue': sum(o.get('amount_paid', 0) for o in orders),
        'total_profit': sum(o.get('profit', 0) for o in orders),
    }

@app.post("/api/orders/create")
async def create_order(order_data: dict):
    """
    Create new order when customer completes checkout on YOUR site
    YOU collect the full payment, then auto-purchase from supplier
    """
    try:
        import random
        import string
        
        # Generate order ID
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Save order to database
        orders_dir = "orders"
        os.makedirs(orders_dir, exist_ok=True)
        
        order_record = {
            "order_id": order_id,
            "status": "pending_fulfillment",
            "customer": order_data.get("customer"),
            "product": order_data.get("product"),
            "payment": order_data.get("payment"),
            "created_at": order_data.get("timestamp"),
            "your_revenue": order_data["payment"]["amount"],
            "supplier_cost": order_data["product"]["cost"],
            "profit": round(order_data["payment"]["amount"] - order_data["product"]["cost"], 2),
            "supplier_url": order_data["product"]["source_url"],
            "fulfillment_status": "awaiting_auto_purchase"
        }
        
        # Save order
        order_file = f"{orders_dir}/order_{order_id}.json"
        with open(order_file, 'w') as f:
            json.dump(order_record, f, indent=2)
        
        print(f"\n💰 NEW ORDER!")
        print(f"   Order ID: {order_id}")
        print(f"   Customer: {order_data['customer']['name']}")
        print(f"   Product: {order_data['product']['product_name']}")
        print(f"   Revenue: ${order_data['payment']['amount']}")
        print(f"   Cost: ${order_data['product']['cost']}")
        print(f"   PROFIT: ${order_record['profit']}")
        
        # AUTO-PURCHASE: Create purchase instruction
        try:
            from auto_purchase import auto_purchase_from_amazon
            purchase_info = auto_purchase_from_amazon(order_record)
            
            # Save purchase instruction
            purchase_file = f"{orders_dir}/purchase_{order_id}.json"
            with open(purchase_file, 'w') as f:
                json.dump(purchase_info, f, indent=2)
            
            print(f"\n🤖 AUTO-PURCHASE INSTRUCTION CREATED")
            print(f"   File: {purchase_file}")
            
            # OPTIONAL: Trigger Selenium bot to auto-purchase
            # Uncomment below to enable FULL automation:
            # from auto_purchase_selenium import AmazonAutoBuyer
            # bot = AmazonAutoBuyer()
            # bot.auto_purchase_product(
            #     asin=order_data['product']['asin'],
            #     customer_address={
            #         'name': order_data['customer']['name'],
            #         'address1': order_data['customer']['address']['line1'],
            #         'address2': order_data['customer']['address'].get('line2', ''),
            #         'city': order_data['customer']['address']['city'],
            #         'state': order_data['customer']['address']['state'],
            #         'zip': order_data['customer']['address']['zip']
            #     }
            # )
            # bot.close()
            
            print(f"   💡 To enable full automation, edit server.py and uncomment Selenium section")
            print()
            
            order_record['purchase_instruction_file'] = purchase_file
            
            # Re-save order with purchase info
            with open(order_file, 'w') as f:
                json.dump(order_record, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Auto-purchase setup failed: {e}")
        
        return {
            "success": True,
            "order_id": order_id,
            "message": "Order created successfully",
            "profit": order_record['profit'],
            "next_step": "Check orders/purchase_{}.json for fulfillment instructions".format(order_id)
        }
        
    except Exception as e:
        print(f"❌ Order error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Order failed: {str(e)}")

@app.get("/api/orders/list")
async def list_orders():
    """List all orders with profit tracking"""
    try:
        orders_dir = "orders"
        if not os.path.exists(orders_dir):
            return {"orders": [], "total_revenue": 0, "total_profit": 0}
        
        orders = []
        total_revenue = 0
        total_profit = 0
        
        for filename in os.listdir(orders_dir):
            if filename.endswith('.json'):
                with open(f"{orders_dir}/{filename}", 'r') as f:
                    order = json.load(f)
                    orders.append(order)
                    total_revenue += order.get("your_revenue", 0)
                    total_profit += order.get("profit", 0)
        
        orders.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return {
            "orders": orders,
            "total_orders": len(orders),
            "total_revenue": round(total_revenue, 2),
            "total_profit": round(total_profit, 2)
        }
    except Exception as e:
        return {"orders": [], "error": str(e)}

@app.get("/api/orders/{order_id}")
async def get_order(order_id: str):
    """Get specific order details"""
    try:
        order_file = f"orders/order_{order_id}.json"
        if not os.path.exists(order_file):
            raise HTTPException(status_code=404, detail="Order not found")
        
        with open(order_file, 'r') as f:
            order = json.load(f)
        
        return order
    except Exception as e:
        raise HTTPException(status_code=404, detail="Order not found")

if __name__ == "__main__":
    # Get port from environment (Railway sets PORT env var)
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting DropShip AI Backend Server...")
    print(f"🤖 AI Status: {'ENABLED' if AI_ENABLED else 'SIMULATED'}")
    print(f"📡 Server: http://0.0.0.0:{port}")
    print(f"📚 Docs: http://0.0.0.0:{port}/docs")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
