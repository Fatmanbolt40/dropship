from fastapi import APIRouter, Depends
from backend.models.schemas import TrendAnalysisRequest, TrendResponse
from backend.services.product_research.trend_analyzer import (
    TrendAnalyzer, 
    CompetitorAnalyzer, 
    NicheValidator,
    ProfitCalculator
)

router = APIRouter()

@router.post("/analyze")
async def analyze_trends(request: TrendAnalysisRequest):
    """Analyze trends for a keyword across multiple platforms"""
    analyzer = TrendAnalyzer()
    
    # Get comprehensive data from all platforms
    full_data = await analyzer.get_all_platform_data(request.keyword)
    
    return full_data

@router.get("/multi-platform/{keyword}")
async def get_multi_platform_analysis(keyword: str):
    """Get comprehensive analysis across all platforms"""
    analyzer = TrendAnalyzer()
    return await analyzer.get_all_platform_data(keyword)

@router.get("/competitors/{niche}")
async def analyze_competitors(niche: str, limit: int = 10):
    """Analyze competitor products in a niche"""
    analyzer = CompetitorAnalyzer()
    products = await analyzer.scrape_competitor_products(niche, limit)
    pricing = await analyzer.analyze_pricing_strategy(niche)
    
    return {
        "niche": niche,
        "competitor_products": products,
        "pricing_analysis": pricing
    }

@router.get("/validate-niche/{niche}")
async def validate_niche(niche: str):
    """Validate if a niche is viable for drop shipping"""
    validator = NicheValidator()
    return await validator.validate_niche(niche)

@router.post("/profit-calculator")
async def calculate_profit(cost: float, price: float, ad_spend: float = 0):
    """Calculate profit margins and ROI"""
    calculator = ProfitCalculator()
    return calculator.calculate_margins(cost, price, ad_spend)

@router.post("/recommend-pricing")
async def recommend_pricing(cost: float, target_margin: float = 50):
    """Get pricing recommendations based on cost and target margin"""
    calculator = ProfitCalculator()
    return calculator.recommend_pricing(cost, target_margin)
