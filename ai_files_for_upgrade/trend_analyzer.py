import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio
from backend.core.redis import get_redis
import json

class TrendAnalyzer:
    """Analyze trends from various platforms"""
    
    def __init__(self):
        self.redis = get_redis()
    
    async def analyze_google_trends(self, keyword: str) -> Dict:
        """Analyze Google Trends data for a keyword"""
        # In production, use pytrends library or Google Trends API
        cache_key = f"trends:google:{keyword}"
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # Simulated trend analysis
        result = {
            "keyword": keyword,
            "platform": "google_trends",
            "trend_score": 75.5,
            "search_volume": 45000,
            "competition_level": "medium",
            "rising_related": ["wireless earbuds", "bluetooth headphones", "noise cancelling"],
            "top_related": ["headphones", "earbuds", "audio"],
            "regional_interest": {
                "US": 100,
                "UK": 75,
                "CA": 80,
                "AU": 70
            }
        }
        
        self.redis.setex(cache_key, 3600, json.dumps(result))
        return result
    
    async def analyze_tiktok_trends(self, keyword: str) -> Dict:
        """Analyze TikTok trends for a keyword"""
        cache_key = f"trends:tiktok:{keyword}"
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # In production, scrape TikTok or use TikTok API
        result = {
            "keyword": keyword,
            "platform": "tiktok",
            "trend_score": 85.2,
            "hashtag_views": 1250000,
            "video_count": 8500,
            "engagement_rate": 12.5,
            "top_creators": ["@techreviewer", "@gadgetguru", "@techtok"],
            "trending_hashtags": ["#" + keyword, "#tech", "#gadgets", "#musthave"]
        }
        
        self.redis.setex(cache_key, 3600, json.dumps(result))
        return result
    
    async def get_combined_trend_score(self, keyword: str) -> float:
        """Get combined trend score from all platforms"""
        google_data = await self.analyze_google_trends(keyword)
        tiktok_data = await self.analyze_tiktok_trends(keyword)
        instagram_data = await self.analyze_instagram_trends(keyword)
        amazon_data = await self.analyze_amazon_trends(keyword)
        
        # Weighted average across all platforms
        google_score = google_data.get("trend_score", 0) * 0.25
        tiktok_score = tiktok_data.get("trend_score", 0) * 0.30
        instagram_score = instagram_data.get("trend_score", 0) * 0.20
        amazon_score = amazon_data.get("trend_score", 0) * 0.25
        
        return round(google_score + tiktok_score + instagram_score + amazon_score, 2)
    
    async def get_all_platform_data(self, keyword: str) -> Dict:
        """Get trend data from all platforms"""
        import asyncio
        platforms = await asyncio.gather(
            self.analyze_google_trends(keyword),
            self.analyze_tiktok_trends(keyword),
            self.analyze_instagram_trends(keyword),
            self.analyze_amazon_trends(keyword),
            self.analyze_ebay_trends(keyword),
            self.analyze_reddit_trends(keyword)
        )
        
        combined_score = await self.get_combined_trend_score(keyword)
        
        return {
            "keyword": keyword,
            "combined_score": combined_score,
            "platforms": {
                "google_trends": platforms[0],
                "tiktok": platforms[1],
                "instagram": platforms[2],
                "amazon": platforms[3],
                "ebay": platforms[4],
                "reddit": platforms[5]
            },
            "recommendation": self._get_recommendation(combined_score),
            "market_insights": self._generate_market_insights(platforms)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on combined score"""
        if score >= 85:
            return "🔥 HIGHLY RECOMMENDED - Extremely hot market, act fast!"
        elif score >= 75:
            return "✅ RECOMMENDED - Strong market demand, good opportunity"
        elif score >= 65:
            return "👍 GOOD - Decent market potential, worth testing"
        elif score >= 50:
            return "⚠️ MODERATE - Average opportunity, requires good execution"
        else:
            return "❌ RISKY - Low market interest, not recommended"
    
    def _generate_market_insights(self, platforms: list) -> Dict:
        """Generate insights from all platform data"""
        return {
            "strongest_platform": max(platforms[:4], key=lambda x: x.get("trend_score", 0))["platform"],
            "total_social_engagement": sum([p.get("engagement_rate", 0) for p in platforms[:2]]),
            "market_maturity": "Growing" if platforms[3].get("trend_score", 0) > 75 else "Mature",
            "competition_analysis": "Medium competition with room for differentiation"
        }
        instagram_score = instagram_data.get("trend_score", 0) * 0.20
        amazon_score = amazon_data.get("trend_score", 0) * 0.25
        
        return round(google_score + tiktok_score + instagram_score + amazon_score, 2)
    
    async def get_all_platform_data(self, keyword: str) -> Dict:
        """Get trend data from all platforms"""
        platforms = await asyncio.gather(
            self.analyze_google_trends(keyword),
            self.analyze_tiktok_trends(keyword),
            self.analyze_instagram_trends(keyword),
            self.analyze_amazon_trends(keyword),
            self.analyze_ebay_trends(keyword),
            self.analyze_reddit_trends(keyword)
        )
        
        combined_score = await self.get_combined_trend_score(keyword)
        
        return {
            "keyword": keyword,
            "combined_score": combined_score,
            "platforms": {
                "google_trends": platforms[0],
                "tiktok": platforms[1],
                "instagram": platforms[2],
                "amazon": platforms[3],
                "ebay": platforms[4],
                "reddit": platforms[5]
            },
            "recommendation": self._get_recommendation(combined_score),
            "market_insights": self._generate_market_insights(platforms)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on combined score"""
        if score >= 85:
            return "🔥 HIGHLY RECOMMENDED - Extremely hot market, act fast!"
        elif score >= 75:
            return "✅ RECOMMENDED - Strong market demand, good opportunity"
        elif score >= 65:
            return "👍 GOOD - Decent market potential, worth testing"
        elif score >= 50:
            return "⚠️ MODERATE - Average opportunity, requires good execution"
        else:
            return "❌ RISKY - Low market interest, not recommended"
    
    def _generate_market_insights(self, platforms: list) -> Dict:
        """Generate insights from all platform data"""
        return {
            "strongest_platform": max(platforms[:4], key=lambda x: x.get("trend_score", 0))["platform"],
            "total_social_engagement": sum([p.get("engagement_rate", 0) for p in platforms[:2]]),
            "market_maturity": "Growing" if platforms[3].get("trend_score", 0) > 75 else "Mature",
            "competition_analysis": "Medium competition with room for differentiation"
        }


import asyncio


class CompetitorAnalyzer:
    """Analyze competitor products and pricing"""
    
    async def scrape_competitor_products(self, niche: str, limit: int = 10) -> List[Dict]:
        """Scrape competitor products from various sources"""
        # In production, use Playwright for dynamic content
        products = []
        
        # Simulated competitor data
        for i in range(limit):
            products.append({
                "title": f"{niche} Product {i+1}",
                "price": round(29.99 + (i * 5), 2),
                "rating": round(4.0 + (i * 0.05), 1),
                "reviews": 150 + (i * 50),
                "seller": f"Seller {i+1}",
                "url": f"https://example.com/product-{i+1}",
                "estimated_sales": 500 + (i * 100)
            })
        
        return products
    
    async def analyze_pricing_strategy(self, niche: str) -> Dict:
        """Analyze competitor pricing and suggest optimal price"""
        competitors = await self.scrape_competitor_products(niche)
        
        if not competitors:
            return {"error": "No competitors found"}
        
        prices = [p["price"] for p in competitors]
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        return {
            "average_price": round(avg_price, 2),
            "min_price": min_price,
            "max_price": max_price,
            "suggested_price": round(avg_price * 0.95, 2),  # Slightly undercut
            "price_range": f"${min_price} - ${max_price}",
            "competitor_count": len(competitors),
            "market_saturation": "medium" if len(competitors) < 20 else "high"
        }


class ProfitCalculator:
    """Calculate profit margins and ROI"""
    
    def calculate_margins(self, cost: float, price: float, ad_spend: float = 0) -> Dict:
        """Calculate detailed profit margins"""
        gross_profit = price - cost
        gross_margin = (gross_profit / price) * 100 if price > 0 else 0
        
        # Account for typical fees
        payment_processing_fee = price * 0.029 + 0.30  # Stripe-like fees
        platform_fee = price * 0.02  # Platform fees
        shipping_cost = cost * 0.1  # Estimated shipping
        
        total_costs = cost + payment_processing_fee + platform_fee + shipping_cost + ad_spend
        net_profit = price - total_costs
        net_margin = (net_profit / price) * 100 if price > 0 else 0
        
        roi = (net_profit / total_costs) * 100 if total_costs > 0 else 0
        
        return {
            "product_cost": round(cost, 2),
            "selling_price": round(price, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin_percent": round(gross_margin, 2),
            "payment_processing_fee": round(payment_processing_fee, 2),
            "platform_fee": round(platform_fee, 2),
            "shipping_cost": round(shipping_cost, 2),
            "ad_spend": round(ad_spend, 2),
            "total_costs": round(total_costs, 2),
            "net_profit": round(net_profit, 2),
            "net_margin_percent": round(net_margin, 2),
            "roi_percent": round(roi, 2),
            "break_even_units": round(ad_spend / net_profit, 0) if net_profit > 0 else 0
        }
    
    def recommend_pricing(self, cost: float, target_margin: float = 50) -> Dict:
        """Recommend pricing based on target margin"""
        # Calculate price needed for target margin
        target_price = cost / (1 - (target_margin / 100))
        
        return {
            "cost": cost,
            "target_margin_percent": target_margin,
            "recommended_price": round(target_price, 2),
            "expected_profit": round(target_price - cost, 2),
            "price_tiers": {
                "budget": round(cost * 1.5, 2),
                "standard": round(cost * 2, 2),
                "premium": round(cost * 3, 2)
            }
        }


class NicheValidator:
    """Validate niche viability"""
    
    def __init__(self):
        self.trend_analyzer = TrendAnalyzer()
        self.competitor_analyzer = CompetitorAnalyzer()
    
    async def validate_niche(self, niche: str) -> Dict:
        """Comprehensive niche validation"""
        trend_score = await self.trend_analyzer.get_combined_trend_score(niche)
        pricing_data = await self.competitor_analyzer.analyze_pricing_strategy(niche)
        
        # Calculate viability score
        viability_factors = {
            "trend_strength": trend_score / 100,
            "market_saturation": 0.7 if pricing_data.get("market_saturation") == "medium" else 0.3,
            "price_point": 0.8 if pricing_data.get("average_price", 0) > 20 else 0.5
        }
        
        viability_score = sum(viability_factors.values()) / len(viability_factors) * 100
        
        recommendation = "EXCELLENT" if viability_score > 75 else \
                        "GOOD" if viability_score > 60 else \
                        "MODERATE" if viability_score > 45 else "POOR"
        
        return {
            "niche": niche,
            "viability_score": round(viability_score, 2),
            "recommendation": recommendation,
            "trend_score": trend_score,
            "market_saturation": pricing_data.get("market_saturation"),
            "average_price": pricing_data.get("average_price"),
            "competitor_count": pricing_data.get("competitor_count"),
            "factors": viability_factors,
            "risks": self._identify_risks(viability_factors),
            "opportunities": self._identify_opportunities(viability_factors)
        }
    
    def _identify_risks(self, factors: Dict) -> List[str]:
        """Identify potential risks"""
        risks = []
        if factors["market_saturation"] < 0.5:
            risks.append("High market saturation - difficult to stand out")
        if factors["trend_strength"] < 0.5:
            risks.append("Low trend strength - declining interest")
        if factors["price_point"] < 0.6:
            risks.append("Low price point - limited profit margins")
        return risks
    
    def _identify_opportunities(self, factors: Dict) -> List[str]:
        """Identify opportunities"""
        opportunities = []
        if factors["trend_strength"] > 0.7:
            opportunities.append("Strong trending interest - high demand potential")
        if factors["market_saturation"] > 0.6:
            opportunities.append("Moderate competition - room for new entrants")
        if factors["price_point"] > 0.7:
            opportunities.append("Good price point - healthy profit potential")
        return opportunities
