#!/usr/bin/env python3
"""
AI Marketing Team - Automated marketing campaigns for dropshipping products
Creates Facebook ads, Instagram posts, TikTok scripts, email campaigns
"""

import os
import json
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AIMarketingTeam:
    """AI-powered marketing automation"""
    
    def __init__(self):
        self.campaigns_dir = "marketing_campaigns"
        os.makedirs(self.campaigns_dir, exist_ok=True)
    
    def create_full_campaign(self, product: Dict) -> Dict:
        """Create complete marketing campaign for a product"""
        
        campaign = {
            'product_name': product['name'],
            'created_at': datetime.now().isoformat(),
            'facebook_ads': self.generate_facebook_ads(product),
            'instagram_posts': self.generate_instagram_posts(product),
            'tiktok_scripts': self.generate_tiktok_scripts(product),
            'email_campaign': self.generate_email_campaign(product),
            'google_ads': self.generate_google_ads(product),
            'pinterest_pins': self.generate_pinterest_pins(product)
        }
        
        # Save campaign
        filename = f"{self.campaigns_dir}/{product['name'].replace(' ', '_').lower()}_{int(datetime.now().timestamp())}.json"
        with open(filename, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        return campaign
    
    def generate_facebook_ads(self, product: Dict) -> List[Dict]:
        """Generate Facebook ad variations"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        discount = round((product.get('cost', 0) / price) * 100) if price > 0 else 30
        
        ads = [
            {
                'headline': f"🔥 {product['name']} - {100-discount}% OFF Today!",
                'primary_text': f"Don't miss out! Get your {product['name']} at an amazing price. ⚡ Fast shipping ⚡ Premium quality ⚡ Money-back guarantee. Limited stock available!",
                'description': f"Only ${price} - Shop now before it's gone!",
                'call_to_action': 'Shop Now',
                'image_suggestion': product.get('image_url', ''),
                'target_audience': {
                    'age': '18-45',
                    'interests': [product.get('niche', 'Shopping'), 'Online Shopping', 'Deals'],
                    'locations': 'USA, Canada, UK, Australia'
                }
            },
            {
                'headline': f"⭐ Premium {product['name']} - Free Shipping",
                'primary_text': f"Transform your life with our top-rated {product['name']}! ✅ {product.get('rating', 4.5)}⭐ rating ✅ Thousands of happy customers ✅ Fast & free delivery. Order yours today!",
                'description': f"Starting at just ${price}!",
                'call_to_action': 'Learn More',
                'image_suggestion': product.get('image_url', ''),
                'target_audience': {
                    'age': '25-55',
                    'interests': [product.get('niche', 'Shopping'), 'Premium Products'],
                    'locations': 'Worldwide'
                }
            },
            {
                'headline': f"🎁 Perfect Gift: {product['name']}",
                'primary_text': f"Looking for the perfect gift? Our {product['name']} is loved by everyone! 💝 Gift-ready packaging 💝 Fast delivery 💝 Satisfaction guaranteed. Make someone's day special!",
                'description': f"Gift it for ${price}",
                'call_to_action': 'Buy Now',
                'image_suggestion': product.get('image_url', ''),
                'target_audience': {
                    'age': '21-60',
                    'interests': ['Gift Shopping', product.get('niche', 'Shopping')],
                    'locations': 'USA, Canada, UK'
                }
            }
        ]
        
        return ads
    
    def generate_instagram_posts(self, product: Dict) -> List[Dict]:
        """Generate Instagram post content"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        
        posts = [
            {
                'caption': f"✨ Just dropped: {product['name']}! ✨\n\n"
                          f"🔥 Trending NOW\n"
                          f"⭐ {product.get('rating', 4.5)}/5 rating\n"
                          f"💰 Only ${price}\n"
                          f"🚚 Fast & free shipping\n\n"
                          f"Tag someone who needs this! 💙\n\n"
                          f"#trending #musthave #shopnow #deals #shopping",
                'image': product.get('image_url', ''),
                'hashtags': f"#trending #musthave #{product.get('niche', 'shopping').lower().replace(' ', '')} #shopnow #deals",
                'post_type': 'Feed Post'
            },
            {
                'caption': f"🎯 DEAL ALERT! 🎯\n\n"
                          f"{product['name']} at an INSANE price!\n\n"
                          f"❤️ Double tap if you want this!\n"
                          f"💬 Comment \"MINE\" for the link\n"
                          f"🔗 Link in bio\n\n"
                          f"Hurry - limited stock! ⏰",
                'image': product.get('image_url', ''),
                'hashtags': f"#sale #dealalert #limitedstock #{product.get('niche', 'shopping').lower()}",
                'post_type': 'Story'
            },
            {
                'caption': f"🌟 Customer favorite! 🌟\n\n"
                          f"Why everyone loves our {product['name']}:\n"
                          f"✅ Premium quality\n"
                          f"✅ Affordable price (${price})\n"
                          f"✅ Fast shipping\n"
                          f"✅ Money-back guarantee\n\n"
                          f"Join thousands of happy customers! 💙",
                'image': product.get('image_url', ''),
                'hashtags': '#customerfavorite #5star #quality #shopsmall',
                'post_type': 'Reel'
            }
        ]
        
        return posts
    
    def generate_tiktok_scripts(self, product: Dict) -> List[Dict]:
        """Generate TikTok video scripts"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        
        scripts = [
            {
                'hook': f"POV: You just discovered the #{product['name'].split()[0]} everyone's talking about 😱",
                'script': f"Okay so I just got this {product['name']} and I'm OBSESSED. "
                         f"Like seriously, for ${price}?? It's literally worth 3x that. "
                         f"Fast shipping, amazing quality, and it actually works! "
                         f"Link in bio before they sell out! ⚡",
                'duration': '15-30 seconds',
                'sounds': ['Trending audio', 'Upbeat music'],
                'effects': ['Fast cuts', 'Product close-ups', 'Before/after'],
                'hashtags': '#tiktokmademebuyit #musthave #amazonfinds #viral'
            },
            {
                'hook': "Things I bought that are actually worth it: Part 27",
                'script': f"Number 1: This {product['name']}. I was skeptical but WOW. "
                         f"It's only ${price} and it changed everything. "
                         f"{product.get('rating', 4.5)} stars for a reason! "
                         f"You NEED this in your life. Trust me.",
                'duration': '20-40 seconds',
                'sounds': ['Voiceover', 'Trending sound'],
                'effects': ['Text overlays', 'Product showcase'],
                'hashtags': '#worthit #productsthatslay #amazonfavorites'
            },
            {
                'hook': "Wait till you see what I got for under $100... 😏",
                'script': f"So I ordered this {product['name']} not expecting much... "
                         f"GUYS. This is a GAME CHANGER. Quality is insane, "
                         f"shipped fast, and it actually does what it says! "
                         f"Already ordering another one for my bestie! Link below 👇",
                'duration': '30-45 seconds',
                'sounds': ['Unboxing music'],
                'effects': ['Unboxing footage', 'Reaction shots'],
                'hashtags': '#unboxing #haul #shopwithme #dealoftheday'
            }
        ]
        
        return scripts
    
    def generate_email_campaign(self, product: Dict) -> Dict:
        """Generate email marketing campaign"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        
        return {
            'subject_lines': [
                f"🔥 JUST IN: {product['name']} - Limited Stock!",
                f"You won't believe this {product['name']} deal...",
                f"⭐ {product.get('rating', 4.5)} stars - See why everyone loves it!",
                f"Last chance: {product['name']} at this price 👀"
            ],
            'email_body': f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h1 style="color: #333;">🎉 Introducing: {product['name']}</h1>
    
    <img src="{product.get('image_url', '')}" style="width: 100%; max-width: 500px;" />
    
    <h2 style="color: #FF6B6B;">Only ${price} - Limited Time!</h2>
    
    <p style="font-size: 16px; line-height: 1.6;">
        We're excited to bring you our newest arrival! This {product['name']} 
        has been flying off the shelves and we can see why:
    </p>
    
    <ul style="font-size: 16px; line-height: 1.8;">
        <li>⭐ {product.get('rating', 4.5)}/5 star rating</li>
        <li>🚚 Fast & FREE shipping</li>
        <li>💯 Money-back guarantee</li>
        <li>🎁 Perfect gift option</li>
    </ul>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="[PRODUCT_LINK]" style="background: #FF6B6B; color: white; padding: 15px 40px; 
           text-decoration: none; border-radius: 5px; font-size: 18px; font-weight: bold;">
            Shop Now →
        </a>
    </div>
    
    <p style="color: #666; font-size: 14px;">
        Don't miss out - stock is limited and selling fast! ⏰
    </p>
</div>
            """,
            'follow_up_sequence': [
                {
                    'day': 1,
                    'subject': f"Still thinking about the {product['name']}? Here's 10% OFF!",
                    'message': "We noticed you were interested! Use code WELCOME10 for 10% off your first order."
                },
                {
                    'day': 3,
                    'subject': f"FINAL HOURS: Your {product['name']} is waiting...",
                    'message': "Last chance to grab this at the current price. Stock running low!"
                },
                {
                    'day': 7,
                    'subject': "See what our customers are saying! ⭐⭐⭐⭐⭐",
                    'message': "Don't just take our word for it - read the 5-star reviews!"
                }
            ]
        }
    
    def generate_google_ads(self, product: Dict) -> List[Dict]:
        """Generate Google Ads campaigns"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        
        return [
            {
                'headline_1': f"{product['name']}",
                'headline_2': f"Only ${price} - Free Ship",
                'headline_3': "⭐ Top Rated Product",
                'description_1': f"Premium {product['name']} at unbeatable prices. Fast shipping, money-back guarantee.",
                'description_2': f"Shop now and save! {product.get('rating', 4.5)}⭐ rating. Thousands of happy customers.",
                'keywords': [
                    f"{product['name'].lower()}",
                    f"buy {product['name'].lower()}",
                    f"{product['name'].lower()} online",
                    f"best {product['name'].lower()}",
                    f"cheap {product['name'].lower()}",
                    f"{product.get('niche', 'products').lower()}"
                ],
                'bid_strategy': 'Maximize Conversions',
                'daily_budget': '$10-20'
            }
        ]
    
    def generate_pinterest_pins(self, product: Dict) -> List[Dict]:
        """Generate Pinterest pin descriptions"""
        price = product.get('suggested_resale_price', product.get('cost', 0))
        
        return [
            {
                'title': f"Must-Have: {product['name']} | ${price}",
                'description': f"Transform your {product.get('niche', 'life').lower()} with this amazing {product['name']}! "
                              f"✨ {product.get('rating', 4.5)}⭐ rating ✨ Fast shipping ✨ Money-back guarantee. "
                              f"Click to shop now! #musthave #shopping #deals",
                'board': product.get('niche', 'Trending Products'),
                'image': product.get('image_url', '')
            },
            {
                'title': f"Deal Alert: {product['name']} Under ${int(price) + 10}!",
                'description': f"Don't miss this incredible deal! Premium {product['name']} at an unbeatable price. "
                              f"Join thousands of happy customers. Shop now! #deals #shopping #sale",
                'board': 'Daily Deals',
                'image': product.get('image_url', '')
            }
        ]

# Global instance
ai_marketing = AIMarketingTeam()

if __name__ == '__main__':
    # Test with sample product
    test_product = {
        'name': 'Wireless Bluetooth Earbuds',
        'cost': 24.99,
        'suggested_resale_price': 49.99,
        'rating': 4.5,
        'niche': 'Electronics',
        'image_url': 'https://example.com/image.jpg'
    }
    
    campaign = ai_marketing.create_full_campaign(test_product)
    print(f"✅ Created marketing campaign for {test_product['name']}")
    print(f"📱 Facebook Ads: {len(campaign['facebook_ads'])}")
    print(f"📸 Instagram Posts: {len(campaign['instagram_posts'])}")
    print(f"🎵 TikTok Scripts: {len(campaign['tiktok_scripts'])}")
    print(f"📧 Email Campaign: Ready")
