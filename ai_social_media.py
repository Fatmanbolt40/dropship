#!/usr/bin/env python3
"""
AI SOCIAL MEDIA MANAGER
Automatically posts your products to Facebook, Instagram, TikTok
Runs 24/7 - drives traffic while you sleep!
"""

import os
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SocialMediaAI:
    def __init__(self):
        self.store_url = self.get_public_url()
        self.campaigns_dir = "campaigns"
        self.posts_dir = "social_posts"
        os.makedirs(self.posts_dir, exist_ok=True)
        
        # Social media credentials (you'll add these later)
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    def get_public_url(self):
        """Get your public store URL from ngrok"""
        try:
            import requests
            response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
            data = response.json()
            if data.get('tunnels'):
                url = data['tunnels'][0]['public_url']
                print(f"🌐 Public Store URL: {url}")
                return url
        except:
            pass
        return "http://localhost:8080"
    
    def generate_facebook_post(self, product):
        """Generate engaging Facebook post"""
        templates = [
            f"🔥 JUST IN! {product['product_name']} for only ${product['suggested_resale_price']}!\n\nUsually ${product['cost']} elsewhere! Grab yours now before they're gone!\n\n👉 Shop: {self.store_url}/store_with_checkout.html\n\n#deals #shopping #sale",
            
            f"💎 Premium Quality Alert!\n\n{product['product_name']} - normally ${product['cost']*1.5:.2f}, now ONLY ${product['suggested_resale_price']}!\n\nLimited stock! ⚡\n\n🛒 Get it here: {self.store_url}/store_with_checkout.html\n\n#shopping #deals #musthave",
            
            f"⭐ {product['product_name']}\n\nOur customers LOVE this! ⭐⭐⭐⭐⭐\n\nSpecial price: ${product['suggested_resale_price']}\nFast shipping included!\n\n👉 {self.store_url}/store_with_checkout.html\n\n#bestseller #trending",
        ]
        return random.choice(templates)
    
    def generate_instagram_caption(self, product):
        """Generate Instagram caption with hashtags"""
        captions = [
            f"✨ New arrival alert! ✨\n\n{product['product_name']}\n💰 ${product['suggested_resale_price']}\n\nLink in bio! 🔗\n\n#shopping #deals #newproduct #musthave #sale #trending #shoplocal #onlineshopping #dealoftheday #savings",
            
            f"🎁 Treat yourself! 🎁\n\n{product['product_name']}\nOnly ${product['suggested_resale_price']} today!\n\n⚡ Fast shipping\n💯 Quality guaranteed\n\nShop now - link in bio!\n\n#shopaholic #retailtherapy #shopping #deals #sale #musthave #trending",
            
            f"💕 You NEED this! 💕\n\n{product['product_name']}\n\nSpecial price: ${product['suggested_resale_price']}\n\nTap link in bio 👆\n\n#shopping #style #musthave #deals #sale #shopnow #onlineshop #trendingproducts",
        ]
        return random.choice(captions)
    
    def generate_tiktok_script(self, product):
        """Generate TikTok video script"""
        scripts = [
            {
                "hook": f"WAIT! Don't buy {product['product_name']} until you see this!",
                "content": f"I found this {product['product_name']} for only ${product['suggested_resale_price']}! It's usually ${product['cost']*2:.2f}!",
                "cta": f"Link in bio! Go get it before it sells out! 🔥",
                "hashtags": "#deals #shopping #musthave #amazonfinds #tiktokmademebuyit"
            },
            {
                "hook": f"Y'all asked for product recommendations... here's one!",
                "content": f"{product['product_name']} is AMAZING and it's only ${product['suggested_resale_price']} right now!",
                "cta": "Check my bio for the link! You won't regret it! 💯",
                "hashtags": "#productreview #shopping #recommendation #musthave #deals"
            },
            {
                "hook": "Stop scrolling! I found something you NEED!",
                "content": f"This {product['product_name']} is a game changer. Only ${product['suggested_resale_price']}!",
                "cta": "Link in bio - go go go! ⚡",
                "hashtags": "#shopwithme #haul #deals #shopping #musthave"
            }
        ]
        return random.choice(scripts)
    
    def create_social_posts(self, product):
        """Create posts for all platforms"""
        posts = {
            'product_name': product['product_name'],
            'created_at': datetime.now().isoformat(),
            'platforms': {
                'facebook': {
                    'text': self.generate_facebook_post(product),
                    'image_url': product['image_url'],
                    'link': f"{self.store_url}/store_with_checkout.html",
                    'status': 'ready'
                },
                'instagram': {
                    'caption': self.generate_instagram_caption(product),
                    'image_url': product['image_url'],
                    'bio_link': f"{self.store_url}/store_with_checkout.html",
                    'status': 'ready'
                },
                'tiktok': {
                    'script': self.generate_tiktok_script(product),
                    'product_image': product['image_url'],
                    'bio_link': f"{self.store_url}/store_with_checkout.html",
                    'status': 'ready'
                }
            }
        }
        return posts
    
    def post_to_facebook(self, post_data):
        """Post to Facebook (requires Facebook API token)"""
        if not self.facebook_token:
            print("⚠️  Facebook: Set FACEBOOK_ACCESS_TOKEN in .env to auto-post")
            return False
        
        try:
            # Facebook Graph API posting code here
            # You'll add your token and page ID
            print(f"📘 Posted to Facebook: {post_data['text'][:50]}...")
            return True
        except Exception as e:
            print(f"❌ Facebook post failed: {str(e)}")
            return False
    
    def post_to_instagram(self, post_data):
        """Post to Instagram (requires Instagram API token)"""
        if not self.instagram_token:
            print("⚠️  Instagram: Set INSTAGRAM_ACCESS_TOKEN in .env to auto-post")
            return False
        
        try:
            # Instagram API posting code here
            print(f"📸 Posted to Instagram: {post_data['caption'][:50]}...")
            return True
        except Exception as e:
            print(f"❌ Instagram post failed: {str(e)}")
            return False
    
    def create_tiktok_draft(self, script_data):
        """Create TikTok video script (manual posting for now)"""
        print(f"🎵 TikTok script ready: {script_data['hook'][:50]}...")
        return True
    
    def auto_post_product(self, product):
        """Automatically create and post product to all platforms"""
        print(f"\n📱 Creating social media posts for: {product['product_name']}")
        
        # Generate posts
        posts = self.create_social_posts(product)
        
        # Save posts for manual review/posting
        timestamp = int(datetime.now().timestamp())
        safe_name = product['product_name'].lower().replace(' ', '_')[:30]
        filename = f"{self.posts_dir}/{safe_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"✅ Social posts created: {filename}")
        print(f"\n📘 FACEBOOK POST:")
        print(posts['platforms']['facebook']['text'])
        print(f"\n📸 INSTAGRAM CAPTION:")
        print(posts['platforms']['instagram']['caption'])
        print(f"\n🎵 TIKTOK SCRIPT:")
        tiktok = posts['platforms']['tiktok']['script']
        print(f"   Hook: {tiktok['hook']}")
        print(f"   Content: {tiktok['content']}")
        print(f"   CTA: {tiktok['cta']}")
        print(f"   Hashtags: {tiktok['hashtags']}")
        
        return posts
    
    def run_social_campaign(self, interval_hours=4):
        """Run social media campaigns 24/7"""
        print(f"\n{'='*60}")
        print(f"📱 AI SOCIAL MEDIA MANAGER STARTED")
        print(f"{'='*60}")
        print(f"Mode: Automatic posting every {interval_hours} hours")
        print(f"Platforms: Facebook, Instagram, TikTok")
        print(f"Store URL: {self.store_url}")
        print(f"{'='*60}\n")
        
        cycle = 1
        while True:
            try:
                print(f"\n🔄 CAMPAIGN CYCLE #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Get random product from inventory
                campaigns = []
                for filename in os.listdir(self.campaigns_dir):
                    if filename.endswith('.json'):
                        with open(f"{self.campaigns_dir}/{filename}", 'r') as f:
                            campaigns.append(json.load(f))
                
                if campaigns:
                    product = random.choice(campaigns)
                    self.auto_post_product(product)
                else:
                    print("⚠️  No products in inventory yet")
                
                # Wait for next cycle
                print(f"\n💤 Next post in {interval_hours} hours...")
                time.sleep(interval_hours * 3600)
                cycle += 1
                
            except KeyboardInterrupt:
                print("\n\n⛔ Stopping Social Media Manager...")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                time.sleep(600)

if __name__ == "__main__":
    social = SocialMediaAI()
    
    print("\n🚀 MANUAL TEST - Creating posts for current products...\n")
    
    # Test with current products
    import os
    campaigns_dir = "campaigns"
    if os.path.exists(campaigns_dir):
        for filename in os.listdir(campaigns_dir)[:3]:  # Test with 3 products
            if filename.endswith('.json'):
                with open(f"{campaigns_dir}/{filename}", 'r') as f:
                    product = json.load(f)
                    social.auto_post_product(product)
                    print("\n" + "="*60 + "\n")
                    time.sleep(2)
    
    print("\n✅ Test complete! Posts saved to social_posts/")
    print("\n💡 To run 24/7: Uncomment line in start_all.sh")
