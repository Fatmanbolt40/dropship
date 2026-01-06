#!/usr/bin/env python3
"""
REAL AliExpress Scraper using Playwright
Bypasses anti-bot protection to get ACTUAL working product links
"""

import asyncio
import random
import re
from playwright.async_api import async_playwright

async def scrape_aliexpress_real():
    """Scrape REAL products from AliExpress using browser automation"""
    
    # Search queries for trending dropshipping products
    searches = [
        "wireless earbuds",
        "smart watch",
        "led strip lights",
        "phone accessories",
        "home decor",
        "fitness equipment",
        "beauty tools",
        "pet accessories"
    ]
    
    products = []
    
    async with async_playwright() as p:
        # Launch browser with stealth mode
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Pick a random search
        search_term = random.choice(searches)
        url = f"https://www.aliexpress.us/w/wholesale-{search_term.replace(' ', '-')}.html?spm=a2g0o.home.search.0"
        
        print(f"🔍 Searching AliExpress for: {search_term}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(3000)  # Wait for JS to load
            
            # Find product cards
            product_cards = await page.query_selector_all('[class*="product-card"]')
            
            if not product_cards:
                # Try alternative selectors
                product_cards = await page.query_selector_all('[class*="search-card-item"]')
            
            print(f"📦 Found {len(product_cards)} product cards")
            
            # Extract up to 10 products
            for card in product_cards[:10]:
                try:
                    # Get product link
                    link_elem = await card.query_selector('a[href*="/item/"]')
                    if not link_elem:
                        continue
                    
                    product_url = await link_elem.get_attribute('href')
                    if not product_url.startswith('http'):
                        product_url = 'https:' + product_url if product_url.startswith('//') else 'https://www.aliexpress.us' + product_url
                    
                    # Get title
                    title_elem = await card.query_selector('[class*="title"]')
                    if not title_elem:
                        title_elem = await card.query_selector('h1, h2, h3')
                    
                    title = await title_elem.inner_text() if title_elem else "Product"
                    title = title.strip()[:80]  # Limit length
                    
                    # Get price
                    price_elem = await card.query_selector('[class*="price"]')
                    price_text = await price_elem.inner_text() if price_elem else "$9.99"
                    
                    # Extract numeric price
                    price_match = re.search(r'[\$]?([\d,]+\.?\d*)', price_text)
                    if price_match:
                        price = float(price_match.group(1).replace(',', ''))
                    else:
                        price = 9.99
                    
                    # Calculate cost (estimate 30-40% of retail price for wholesale)
                    cost = round(price * random.uniform(0.30, 0.40), 2)
                    
                    # Get image
                    img_elem = await card.query_selector('img')
                    img_url = await img_elem.get_attribute('src') if img_elem else ""
                    if img_url and not img_url.startswith('http'):
                        img_url = 'https:' + img_url
                    
                    products.append({
                        'name': title,
                        'cost': cost,
                        'retail_price': price,
                        'url': product_url,
                        'image': img_url,
                        'source': 'AliExpress'
                    })
                    
                    print(f"✅ {title[:50]}... - ${cost} → ${price}")
                    
                except Exception as e:
                    print(f"⚠️  Error extracting product: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error loading page: {e}")
        
        finally:
            await browser.close()
    
    return products


async def main():
    """Test the scraper"""
    products = await scrape_aliexpress_real()
    
    print(f"\n🎉 Successfully scraped {len(products)} REAL products!")
    print("\nSample products:")
    for p in products[:3]:
        print(f"\n📦 {p['name']}")
        print(f"   Cost: ${p['cost']} | Retail: ${p['retail_price']}")
        print(f"   Link: {p['url'][:80]}...")


if __name__ == "__main__":
    asyncio.run(main())
