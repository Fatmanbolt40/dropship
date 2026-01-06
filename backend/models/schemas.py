from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# Product Schemas
class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    cost: float
    category: Optional[str] = None
    niche: Optional[str] = None
    tags: Optional[List[str]] = []
    image_urls: Optional[List[str]] = []
    aliexpress_url: Optional[str] = None

class ProductCreate(ProductBase):
    supplier_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    profit_margin: float
    trending_score: float
    viral_potential: float
    competition_score: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    platform: str
    supplier_url: Optional[str] = None

class SupplierCreate(SupplierBase):
    contact_info: Optional[Dict] = {}

class SupplierResponse(SupplierBase):
    id: int
    reliability_score: float
    avg_shipping_days: Optional[int] = None
    product_quality_score: float
    communication_score: float
    total_orders: int
    positive_reviews: int
    total_reviews: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Trend Schemas
class TrendAnalysisRequest(BaseModel):
    keyword: str
    platforms: List[str] = ["tiktok", "google_trends"]

class TrendResponse(BaseModel):
    keyword: str
    platform: str
    trend_score: float
    search_volume: int
    competition_level: str
    insights: Dict
    
# Marketing Schemas
class AdCopyRequest(BaseModel):
    product_title: str
    product_description: str
    target_audience: Optional[str] = None
    platform: str = "facebook"

class AdCopyResponse(BaseModel):
    headlines: List[str]
    body_copy: List[str]
    call_to_actions: List[str]
    target_audiences: List[Dict]

# Analytics Schemas
class SalesForecastRequest(BaseModel):
    product_id: int
    days_ahead: int = 30

class SalesForecastResponse(BaseModel):
    product_id: int
    forecast_data: List[Dict]
    confidence_score: float
    total_predicted_sales: float
    total_predicted_revenue: float
