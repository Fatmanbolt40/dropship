from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.schemas import SalesForecastRequest, SalesForecastResponse
from backend.services.analytics.forecasting import (
    SalesForecaster,
    ROIAnalyzer,
    CustomerBehaviorAnalyzer,
    DashboardMetrics
)

router = APIRouter()

@router.post("/forecast-sales", response_model=SalesForecastResponse)
async def forecast_sales(request: SalesForecastRequest, db: Session = Depends(get_db)):
    """Forecast future sales for a product"""
    forecaster = SalesForecaster(db)
    return forecaster.forecast_sales(request.product_id, request.days_ahead)

@router.get("/roi/{product_id}")
async def calculate_roi(product_id: int, period_days: int = 30, db: Session = Depends(get_db)):
    """Calculate ROI for a product"""
    analyzer = ROIAnalyzer(db)
    return analyzer.calculate_product_roi(product_id, period_days)

@router.get("/top-performers")
async def get_top_performers(limit: int = 10, db: Session = Depends(get_db)):
    """Get top performing products"""
    analyzer = ROIAnalyzer(db)
    return {"top_products": analyzer.get_top_performing_products(limit)}

@router.get("/conversion-funnel/{product_id}")
async def analyze_conversion_funnel(product_id: int, period_days: int = 30, db: Session = Depends(get_db)):
    """Analyze conversion funnel for a product"""
    analyzer = CustomerBehaviorAnalyzer()
    return analyzer.analyze_conversion_funnel(product_id, period_days)

@router.get("/dashboard")
async def get_dashboard_metrics(period_days: int = 30, db: Session = Depends(get_db)):
    """Get overall dashboard metrics"""
    metrics = DashboardMetrics(db)
    return metrics.get_overview_metrics(period_days)
