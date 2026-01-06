#!/usr/bin/env python3
"""
Auto-Listing Service
Automatically lists products on multiple platforms (Shopify, eBay, Etsy, etc.)
"""

import json
import os
from datetime import datetime

class AutoLister:
    def __init__(self):
        self.platforms = {
            'shopify': False,  # Will be enabled when API key is added
            'ebay': False,
            'etsy': False,
            'facebook_marketplace': False,
            'poshmark': False
        }
    
    def create_shopify_listing(self, campaign):
        """Create Shopify product listing"""
        product = campaign['product']
        content = campaign['content']
        
        shopify_data = {
            "product": {
                "title": product['name'],
                "body_html": content['description'].replace('\n', '<br>'),
                "vendor": "DropShip AI",
                "product_type": product['niche'],
                "tags": ", ".join([product['niche'], product['source']]),
                "variants": [{
                    "price": str(product.get('suggested_resale_price', product['retail_price'] * 2.5)),
                    "cost": str(product['cost']),
                    "compare_at_price": str(product.get('suggested_resale_price', 0) * 1.3),
                    "inventory_management": "shopify",
                    "inventory_quantity": 999
                }],
                "images": [{
                    "src": product.get('image_url', '')
                }] if product.get('image_url') else [],
                "metafields": [{
                    "key": "source_url",
                    "value": product.get('source_url', ''),
                    "type": "string",
                    "namespace": "supplier"
                }]
            }
        }
        
        return shopify_data
    
    def create_ebay_listing(self, campaign):
        """Create eBay listing format"""
        product = campaign['product']
        content = campaign['content']
        
        ebay_data = {
            "Item": {
                "Title": product['name'][:80],  # eBay title limit
                "Description": self._format_ebay_description(content['description']),
                "PrimaryCategory": {"CategoryID": "0"},  # Would need category mapping
                "StartPrice": str(product.get('suggested_resale_price', product['retail_price'] * 2.5)),
                "CategoryMappingAllowed": "true",
                "Country": "US",
                "Currency": "USD",
                "DispatchTimeMax": "3",
                "ListingDuration": "GTC",
                "ListingType": "FixedPriceItem",
                "PaymentMethods": "PayPal",
                "PictureDetails": {
                    "PictureURL": [product.get('image_url', '')]
                },
                "Quantity": "999",
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30"
                },
                "ShippingDetails": {
                    "ShippingType": "Flat",
                    "ShippingServiceOptions": {
                        "ShippingService": "USPSPriority",
                        "ShippingServiceCost": "0.00"
                    }
                }
            }
        }
        
        return ebay_data
    
    def create_facebook_marketplace_listing(self, campaign):
        """Create Facebook Marketplace listing"""
        product = campaign['product']
        content = campaign['content']
        
        fb_data = {
            "title": product['name'],
            "description": content['description'],
            "price": str(product.get('suggested_resale_price', product['retail_price'] * 2.5)),
            "category": product['niche'],
            "condition": "NEW",
            "availability": "IN_STOCK",
            "images": [product.get('image_url', '')],
            "url": product.get('source_url', '')
        }
        
        return fb_data
    
    def _format_ebay_description(self, description):
        """Format description for eBay HTML"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h2 style="color: #333;">Product Description</h2>
            <p style="line-height: 1.6;">{description.replace(chr(10), '<br>')}</p>
            <hr style="margin: 20px 0;">
            <h3>Shipping Information</h3>
            <ul>
                <li>Free Shipping</li>
                <li>Ships within 1-3 business days</li>
                <li>30-day money-back guarantee</li>
            </ul>
        </div>
        """
        return html
    
    def generate_all_listings(self, campaign_file):
        """Generate listing data for all platforms"""
        with open(campaign_file, 'r') as f:
            campaign = json.load(f)
        
        listings = {
            'shopify': self.create_shopify_listing(campaign),
            'ebay': self.create_ebay_listing(campaign),
            'facebook': self.create_facebook_marketplace_listing(campaign),
            'product_info': campaign['product'],
            'generated_at': datetime.now().isoformat()
        }
        
        # Save listings
        listing_file = campaign_file.replace('campaigns/', 'listings/').replace('.json', '_listings.json')
        os.makedirs('listings', exist_ok=True)
        
        with open(listing_file, 'w') as f:
            json.dump(listings, f, indent=2)
        
        return listings

if __name__ == "__main__":
    # Example usage
    lister = AutoLister()
    
    import glob
    campaigns = glob.glob('campaigns/*.json')
    
    if campaigns:
        print(f"📦 Generating listings for {len(campaigns)} campaigns...")
        for campaign_file in campaigns[:5]:
            try:
                listings = lister.generate_all_listings(campaign_file)
                print(f"✅ Created listings for: {listings['product_info']['name']}")
            except Exception as e:
                print(f"❌ Error: {e}")
    else:
        print("No campaigns found")
