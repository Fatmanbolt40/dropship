from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    cost = Column(Float)
    profit_margin = Column(Float)
    category = Column(String, index=True)
    niche = Column(String, index=True)
    tags = Column(JSON)
    image_urls = Column(JSON)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    aliexpress_url = Column(String)
    trending_score = Column(Float, default=0.0)
    viral_potential = Column(Float, default=0.0)
    competition_score = Column(Float, default=0.0)
    status = Column(String, default="research")  # research, active, paused, discontinued
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    supplier = relationship("Supplier", back_populates="products")
    analytics = relationship("ProductAnalytics", back_populates="product")


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    platform = Column(String)  # aliexpress, cj, alibaba
    supplier_url = Column(String)
    reliability_score = Column(Float, default=0.0)
    avg_shipping_days = Column(Integer)
    product_quality_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    positive_reviews = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    contact_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    products = relationship("Product", back_populates="supplier")


class ProductAnalytics(Base):
    __tablename__ = "product_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    ad_spend = Column(Float, default=0.0)
    roi = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    product = relationship("Product", back_populates="analytics")


class TrendData(Base):
    __tablename__ = "trend_data"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    platform = Column(String)  # tiktok, instagram, google_trends
    trend_score = Column(Float)
    search_volume = Column(Integer, default=0)
    competition_level = Column(String)  # low, medium, high
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    campaign_name = Column(String)
    platform = Column(String)  # facebook, tiktok, google
    ad_copy = Column(Text)
    target_audience = Column(JSON)
    budget = Column(Float)
    status = Column(String, default="draft")  # draft, active, paused, completed
    performance_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StoreProduct(Base):
    __tablename__ = "store_products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform = Column(String)  # shopify, woocommerce
    platform_product_id = Column(String)
    store_url = Column(String)
    current_price = Column(Float)
    inventory_status = Column(String)
    last_synced = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
