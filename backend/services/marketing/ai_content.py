from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from typing import Dict, List
from backend.core.config import settings

class AIContentGenerator:
    """Generate marketing content using AI"""
    
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
    
    async def generate_product_description(self, product_title: str, features: List[str], target_audience: str = "general") -> str:
        """Generate SEO-optimized product description"""
        
        prompt = f"""Write a compelling, SEO-optimized product description for: {product_title}

Key Features:
{chr(10).join(f'- {feature}' for feature in features)}

Target Audience: {target_audience}

Requirements:
- Include emotional triggers
- Highlight benefits, not just features
- Use power words
- Include a call-to-action
- 150-200 words
- SEO-friendly keywords naturally integrated"""

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            # Fallback template
            return f"""Discover the ultimate {product_title} that transforms your daily experience. 
            
Featuring {', '.join(features[:3])}, this premium product is designed for {target_audience} who demand quality and performance.

Perfect for those who appreciate excellence, our {product_title} combines cutting-edge technology with user-friendly design. Whether you're at home, work, or on the go, enjoy unmatched convenience and reliability.

Don't settle for less. Order now and experience the difference!"""
    
    async def generate_ad_copy(self, product_title: str, product_description: str, platform: str = "facebook") -> Dict:
        """Generate ad copy for various platforms"""
        
        prompt = f"""Create compelling ad copy for {platform} advertising.

Product: {product_title}
Description: {product_description}

Generate:
1. 5 attention-grabbing headlines (max 40 characters each)
2. 3 body copy variations (max 125 characters each)
3. 5 call-to-action phrases
4. 3 target audience suggestions with demographics

Make it persuasive, benefit-focused, and optimized for {platform}."""

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            
            # Parse response (simplified)
            return {
                "headlines": [
                    f"🔥 {product_title} - Limited Stock!",
                    f"Transform Your Life with {product_title}",
                    f"Don't Miss Out on {product_title}",
                    f"✨ Premium {product_title} On Sale",
                    f"Get Yours Before It's Gone!"
                ],
                "body_copy": [
                    f"Experience the difference with {product_title}. Premium quality, unbeatable price. Shop now!",
                    f"Why settle for less? {product_title} delivers excellence. Limited time offer!",
                    f"Join thousands of satisfied customers. Get your {product_title} today!"
                ],
                "cta": [
                    "Shop Now",
                    "Get 40% Off Today",
                    "Limited Time Offer",
                    "Claim Your Discount",
                    "Order Now - Free Shipping"
                ],
                "audiences": [
                    {"name": "Tech Enthusiasts", "age": "25-45", "interests": ["technology", "gadgets", "innovation"]},
                    {"name": "Value Shoppers", "age": "30-55", "interests": ["deals", "shopping", "quality products"]},
                    {"name": "Early Adopters", "age": "18-35", "interests": ["trends", "lifestyle", "new products"]}
                ]
            }
        else:
            # Fallback ad copy
            return {
                "headlines": [
                    f"🔥 {product_title} - Limited Stock!",
                    f"Transform Your Life with {product_title}",
                    f"Don't Miss Out on {product_title}",
                    f"✨ Premium {product_title} On Sale",
                    f"Get Yours Before It's Gone!"
                ],
                "body_copy": [
                    f"Experience the difference with {product_title}. Premium quality, unbeatable price.",
                    f"Why settle for less? {product_title} delivers excellence every time.",
                    f"Join thousands of satisfied customers. Get yours today!"
                ],
                "cta": [
                    "Shop Now",
                    "Get 40% Off",
                    "Limited Offer",
                    "Order Today",
                    "Free Shipping"
                ],
                "audiences": [
                    {"name": "General Audience", "age": "25-45", "interests": ["shopping", "quality"]}
                ]
            }
    
    async def generate_video_script(self, product_title: str, key_benefits: List[str], duration: int = 30) -> Dict:
        """Generate TikTok/Instagram video script"""
        
        prompt = f"""Create a {duration}-second video script for TikTok/Instagram Reels.

Product: {product_title}
Key Benefits: {', '.join(key_benefits)}

Include:
1. Hook (first 3 seconds)
2. Problem/Solution
3. Product showcase
4. Call-to-action
5. Suggested visuals
6. Background music style
7. Text overlays

Make it engaging, fast-paced, and thumb-stopping."""

        return {
            "duration_seconds": duration,
            "hook": f"Wait! Before you buy {product_title}, watch this!",
            "sections": [
                {
                    "time": "0-3s",
                    "voiceover": f"Struggling with [problem]? I found the solution!",
                    "visual": "Show problem scenario",
                    "text_overlay": "You NEED This! 😱"
                },
                {
                    "time": "3-10s",
                    "voiceover": f"Meet {product_title} - it changed everything for me",
                    "visual": "Unboxing/reveal product",
                    "text_overlay": f"{product_title} ✨"
                },
                {
                    "time": "10-20s",
                    "voiceover": f"Check out these amazing features: {', '.join(key_benefits[:3])}",
                    "visual": "Quick demo of features",
                    "text_overlay": "Game Changer! 🔥"
                },
                {
                    "time": "20-30s",
                    "voiceover": "And the best part? It's on sale right now!",
                    "visual": "Show price/discount",
                    "text_overlay": "Link in Bio! 🛒"
                }
            ],
            "cta": "Link in bio - Limited stock!",
            "music_style": "Upbeat, trending audio",
            "hashtags": ["#" + product_title.replace(" ", ""), "#trending", "#musthave", "#viral", "#fyp"]
        }
    
    async def generate_email_sequence(self, product_title: str, customer_name: str = "[Name]") -> List[Dict]:
        """Generate email marketing sequence"""
        
        emails = [
            {
                "sequence_number": 1,
                "timing": "Immediately after signup",
                "subject": f"Welcome! Here's your exclusive {product_title} discount 🎁",
                "preview_text": "Get 20% off your first order",
                "body": f"""Hi {customer_name},

Welcome to our community! We're thrilled to have you.

As a special thank you, here's an exclusive 20% discount on {product_title}:

CODE: WELCOME20

Why our customers love {product_title}:
✓ Premium quality
✓ Fast shipping
✓ 30-day money-back guarantee

Don't wait - this offer expires in 24 hours!

[Shop Now Button]

Questions? Just reply to this email.

Best,
The Team""",
                "cta": "Shop Now"
            },
            {
                "sequence_number": 2,
                "timing": "24 hours later if no purchase",
                "subject": f"Your {product_title} discount expires soon ⏰",
                "preview_text": "Last chance for 20% off",
                "body": f"""Hey {customer_name},

Just a friendly reminder - your exclusive 20% discount expires tonight!

Over 1,000 customers have already grabbed theirs. Don't miss out!

Use code: WELCOME20

[Shop Now Button]

Still not sure? Check out our 5-star reviews!

Best,
The Team""",
                "cta": "Shop Now"
            },
            {
                "sequence_number": 3,
                "timing": "3 days later",
                "subject": "Here's what you're missing...",
                "preview_text": f"Real {product_title} stories from our customers",
                "body": f"""Hi {customer_name},

See what our customers are saying about {product_title}:

⭐⭐⭐⭐⭐ "Game changer! Wish I bought it sooner."
⭐⭐⭐⭐⭐ "Amazing quality for the price."
⭐⭐⭐⭐⭐ "Exactly what I needed!"

Ready to join them?

[Shop Now Button]

Best,
The Team""",
                "cta": "See More Reviews"
            }
        ]
        
        return emails


class AudienceTargeting:
    """AI-powered audience identification and targeting"""
    
    async def identify_target_audience(self, product_category: str, price_point: float) -> List[Dict]:
        """Identify potential target audiences"""
        
        # Analyze product and suggest audiences
        audiences = []
        
        if price_point < 20:
            audiences.append({
                "segment": "Budget-Conscious Shoppers",
                "age_range": "18-35",
                "income": "$20k-$50k",
                "interests": ["deals", "discounts", "value shopping"],
                "platforms": ["TikTok", "Instagram", "Facebook"],
                "ad_strategy": "Emphasize price and value"
            })
        
        if price_point > 50:
            audiences.append({
                "segment": "Premium Buyers",
                "age_range": "30-55",
                "income": "$75k+",
                "interests": ["quality", "luxury", "premium products"],
                "platforms": ["Instagram", "Pinterest", "Google"],
                "ad_strategy": "Emphasize quality and exclusivity"
            })
        
        audiences.append({
            "segment": "Early Adopters",
            "age_range": "22-40",
            "income": "$40k-$100k",
            "interests": ["trends", "innovation", "new products"],
            "platforms": ["TikTok", "Instagram", "YouTube"],
            "ad_strategy": "Emphasize uniqueness and trending status"
        })
        
        return audiences
