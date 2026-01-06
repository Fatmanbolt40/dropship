"""
AliExpress Web Scraper - Test Script

This script tests the real web scraping functionality for AliExpress.
It will attempt to scrape live product data and display results.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.supplier_management.supplier_api import AliExpressAPI

async def test_scraper():
    """Test the AliExpress scraper"""
    
    print("=" * 60)
    print("🔍 Testing AliExpress Web Scraper")
    print("=" * 60)
    print()
    
    api = AliExpressAPI()
    
    # Test keywords
    keywords = [
        "wireless earbuds",
        "phone case",
        "smartwatch"
    ]
    
    for keyword in keywords:
        print(f"\n📦 Searching for: '{keyword}'")
        print("-" * 60)
        
        try:
            products = await api.search_products(keyword, page=1, page_size=5)
            
            print(f"✅ Found {len(products)} products\n")
            
            for i, product in enumerate(products[:3], 1):
                print(f"{i}. {product['title'][:60]}...")
                print(f"   💰 Price: ${product['price']}")
                print(f"   ⭐ Rating: {product['rating']}/5")
                print(f"   📦 Orders: {product['orders']}")
                print(f"   🔗 URL: {product['url'][:50]}...")
                print()
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("=" * 60)
    print("✅ Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_scraper())
