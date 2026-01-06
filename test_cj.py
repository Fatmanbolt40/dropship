#!/usr/bin/env python3
from cj_api import CJDropshippingAPI
import os
from dotenv import load_dotenv

load_dotenv()

api = CJDropshippingAPI(os.getenv('CJ_EMAIL'), os.getenv('CJ_API_KEY'))
print('Testing CJ Dropshipping API...')

try:
    products = api.search_products('bluetooth earbuds', page=1, page_size=5)
    print(f'\nFound {len(products)} products:\n')
    
    for i, p in enumerate(products[:3], 1):
        print(f"{i}. {p['name']}")
        print(f"   Price: ${p['price']}")
        print(f"   URL: {p['url']}")
        print(f"   Image: {p['image']}")
        print()
    
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
