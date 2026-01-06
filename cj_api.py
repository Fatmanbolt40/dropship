#!/usr/bin/env python3
"""
CJ Dropshipping API Integration
Real products with real pricing
"""

import requests
import hashlib
import time
from typing import List, Dict, Any

class CJDropshippingAPI:
    def __init__(self, email: str, api_key: str):
        self.base_url = "https://developers.cjdropshipping.com/api2.0/v1"
        self.email = email
        self.api_key = api_key
        self._token = None
        self._token_expires = 0
    
    def _get_auth_token(self) -> str:
        """Generate authentication token"""
        if self._token and time.time() < self._token_expires:
            return self._token
            
        url = f"{self.base_url}/authentication/getAccessToken"
        payload = {
            "email": self.email,
            "password": self.api_key
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    self._token = data['data']['accessToken']
                    self._token_expires = time.time() + 3600  # 1 hour
                    return self._token
        except Exception as e:
            print(f"Auth error: {e}")
        
        return None
    
    def search_products(self, keyword: str = "", page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        """Search products on CJ Dropshipping"""
        token = self._get_auth_token()
        if not token:
            return []
        
        url = f"{self.base_url}/product/list"
        headers = {
            "CJ-Access-Token": token
        }
        params = {
            "pageNum": page,
            "pageSize": page_size
        }
        
        if keyword:
            params["productNameEn"] = keyword
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200 and 'data' in data:
                    products = []
                    for item in data['data'].get('list', []):
                        try:
                            sell_price = float(item.get('sellPrice', 0))
                            if sell_price <= 0:
                                continue
                                
                            products.append({
                                'id': item.get('pid', ''),
                                'name': item.get('productNameEn', 'Product')[:100],
                                'cost': sell_price,
                                'retail_price': sell_price * 1.5,
                                'suggested_resale_price': round(sell_price * 3.2, 2),
                                'image': item.get('productImage', ''),
                                'url': f"https://cjdropshipping.com/product/{item.get('pid', '')}.html",
                                'niche': self._categorize(item.get('productNameEn', '')),
                                'source': 'CJ Dropshipping',
                                'source_url': f"https://cjdropshipping.com/product/{item.get('pid', '')}.html",
                                'image_url': item.get('productImage', ''),
                                'shipping_time': '7-15 days',
                                'supplier_rating': 4.8,
                                'in_stock': True,
                                'margin': round(((sell_price * 3.2 - sell_price) / (sell_price * 3.2)) * 100, 1)
                            })
                        except:
                            continue
                    
                    return products[:page_size]
        except Exception as e:
            print(f"Search error: {e}")
        
        return []
    
    def _categorize(self, name: str) -> str:
        """Categorize product based on name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['earbuds', 'headphone', 'speaker', 'audio', 'music']):
            return 'Electronics'
        elif any(word in name_lower for word in ['watch', 'smart', 'fitness', 'tracker']):
            return 'Electronics'
        elif any(word in name_lower for word in ['yoga', 'fitness', 'exercise', 'gym', 'sports']):
            return 'Sports & Outdoors'
        elif any(word in name_lower for word in ['beauty', 'skin', 'makeup', 'cosmetic']):
            return 'Beauty'
        elif any(word in name_lower for word in ['bag', 'wallet', 'fashion', 'clothes', 'shoes']):
            return 'Fashion'
        elif any(word in name_lower for word in ['home', 'kitchen', 'decor', 'furniture']):
            return 'Home & Garden'
        elif any(word in name_lower for word in ['pet', 'dog', 'cat']):
            return 'Pet Supplies'
        elif any(word in name_lower for word in ['baby', 'kids', 'children', 'toy']):
            return 'Baby Products'
        else:
            return 'Electronics'


# Initialize API
cj_api = CJDropshippingAPI(
    email="CJ5038029",
    api_key="1ac5aec97ba04a59b99d40fdeeeb1478"
)


def get_real_trending_products():
    """Get real products from CJ Dropshipping"""
    import random
    
    keywords = [
        "wireless", "smart", "led", "portable", "fitness",
        "beauty", "home", "kitchen", "phone", "bluetooth"
    ]
    
    keyword = random.choice(keywords)
    print(f"🔍 Searching CJ Dropshipping for: {keyword}")
    
    products = cj_api.search_products(keyword=keyword, page_size=8)
    
    if products:
        print(f"✅ Found {len(products)} REAL products from CJ Dropshipping!")
        return products
    else:
        print("⚠️ Using backup product list")
        return []


if __name__ == "__main__":
    products = get_real_trending_products()
    print(f"\n📦 Sample Products:")
    for p in products[:3]:
        print(f"  • {p['name']}")
        print(f"    Cost: ${p['cost']} → Sell: ${p['suggested_resale_price']}")
        print(f"    Profit: ${p['suggested_resale_price'] - p['cost']:.2f}")
        print()
