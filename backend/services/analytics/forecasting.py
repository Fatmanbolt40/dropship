import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models.models import ProductAnalytics, Product

class SalesForecaster:
    """Forecast future sales using historical data"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def forecast_sales(self, product_id: int, days_ahead: int = 30) -> Dict:
        """Forecast sales for the next N days"""
        
        # Get historical data
        analytics = self.db.query(ProductAnalytics).filter(
            ProductAnalytics.product_id == product_id
        ).order_by(ProductAnalytics.date).all()
        
        if len(analytics) < 7:
            return {
                "error": "Insufficient data for forecasting",
                "minimum_required": 7,
                "current_data_points": len(analytics)
            }
        
        # Prepare data
        dates = [a.date for a in analytics]
        sales = [a.sales for a in analytics]
        
        # Convert to numeric for regression
        X = np.array(range(len(sales))).reshape(-1, 1)
        y = np.array(sales)
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate forecast
        future_X = np.array(range(len(sales), len(sales) + days_ahead)).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        # Get product price for revenue calculation
        product = self.db.query(Product).filter(Product.id == product_id).first()
        price = product.price if product else 0
        
        forecast_data = []
        for i, pred_sales in enumerate(forecast):
            forecast_date = dates[-1] + timedelta(days=i+1)
            forecast_data.append({
                "date": forecast_date.isoformat(),
                "predicted_sales": max(0, int(pred_sales)),
                "predicted_revenue": max(0, round(pred_sales * price, 2))
            })
        
        total_sales = sum([f["predicted_sales"] for f in forecast_data])
        total_revenue = sum([f["predicted_revenue"] for f in forecast_data])
        
        # Calculate confidence based on R²
        r_squared = model.score(X, y)
        
        return {
            "product_id": product_id,
            "forecast_period_days": days_ahead,
            "forecast_data": forecast_data,
            "total_predicted_sales": total_sales,
            "total_predicted_revenue": round(total_revenue, 2),
            "confidence_score": round(r_squared * 100, 2),
            "model_accuracy": f"{round(r_squared * 100, 1)}%"
        }


class ROIAnalyzer:
    """Analyze return on investment for products"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_product_roi(self, product_id: int, period_days: int = 30) -> Dict:
        """Calculate ROI for a product over a period"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        
        analytics = self.db.query(ProductAnalytics).filter(
            ProductAnalytics.product_id == product_id,
            ProductAnalytics.date >= cutoff_date
        ).all()
        
        if not analytics:
            return {"error": "No data available for the specified period"}
        
        total_revenue = sum([a.revenue for a in analytics])
        total_ad_spend = sum([a.ad_spend for a in analytics])
        total_sales = sum([a.sales for a in analytics])
        
        product = self.db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {"error": "Product not found"}
        
        total_cost = product.cost * total_sales
        gross_profit = total_revenue - total_cost
        net_profit = gross_profit - total_ad_spend
        
        roi = (net_profit / (total_cost + total_ad_spend)) * 100 if (total_cost + total_ad_spend) > 0 else 0
        roas = (total_revenue / total_ad_spend) if total_ad_spend > 0 else 0
        
        return {
            "product_id": product_id,
            "period_days": period_days,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_ad_spend": round(total_ad_spend, 2),
            "gross_profit": round(gross_profit, 2),
            "net_profit": round(net_profit, 2),
            "roi_percent": round(roi, 2),
            "roas": round(roas, 2),
            "total_sales": total_sales,
            "average_sale_value": round(total_revenue / total_sales, 2) if total_sales > 0 else 0
        }
    
    def get_top_performing_products(self, limit: int = 10) -> List[Dict]:
        """Get top performing products by ROI"""
        
        # Get all products with recent analytics
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        products = self.db.query(Product).join(ProductAnalytics).filter(
            ProductAnalytics.date >= cutoff_date
        ).distinct().all()
        
        performance = []
        
        for product in products:
            roi_data = self.calculate_product_roi(product.id, 30)
            if "error" not in roi_data:
                performance.append({
                    "product_id": product.id,
                    "product_title": product.title,
                    "roi": roi_data["roi_percent"],
                    "net_profit": roi_data["net_profit"],
                    "total_sales": roi_data["total_sales"]
                })
        
        # Sort by ROI
        performance.sort(key=lambda x: x["roi"], reverse=True)
        
        return performance[:limit]


class CustomerBehaviorAnalyzer:
    """Analyze customer behavior patterns"""
    
    def analyze_conversion_funnel(self, product_id: int, period_days: int = 30) -> Dict:
        """Analyze conversion funnel for a product"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        
        analytics = self.db.query(ProductAnalytics).filter(
            ProductAnalytics.product_id == product_id,
            ProductAnalytics.date >= cutoff_date
        ).all()
        
        if not analytics:
            return {"error": "No data available"}
        
        total_views = sum([a.views for a in analytics])
        total_clicks = sum([a.clicks for a in analytics])
        total_sales = sum([a.sales for a in analytics])
        
        click_rate = (total_clicks / total_views * 100) if total_views > 0 else 0
        conversion_rate = (total_sales / total_clicks * 100) if total_clicks > 0 else 0
        overall_conversion = (total_sales / total_views * 100) if total_views > 0 else 0
        
        return {
            "product_id": product_id,
            "period_days": period_days,
            "funnel": {
                "impressions": total_views,
                "clicks": total_clicks,
                "purchases": total_sales
            },
            "metrics": {
                "click_through_rate": round(click_rate, 2),
                "conversion_rate": round(conversion_rate, 2),
                "overall_conversion_rate": round(overall_conversion, 2)
            },
            "drop_off": {
                "view_to_click": f"{round(100 - click_rate, 2)}%",
                "click_to_purchase": f"{round(100 - conversion_rate, 2)}%"
            },
            "recommendations": self._get_funnel_recommendations(click_rate, conversion_rate)
        }
    
    def _get_funnel_recommendations(self, click_rate: float, conversion_rate: float) -> List[str]:
        """Get recommendations based on funnel performance"""
        recommendations = []
        
        if click_rate < 2:
            recommendations.append("Low click-through rate - improve product images and titles")
        elif click_rate < 5:
            recommendations.append("Average CTR - A/B test different images and descriptions")
        
        if conversion_rate < 1:
            recommendations.append("Low conversion - review pricing and product page quality")
        elif conversion_rate < 3:
            recommendations.append("Moderate conversion - add customer reviews and trust signals")
        
        if not recommendations:
            recommendations.append("Strong performance - scale up advertising budget")
        
        return recommendations


class DashboardMetrics:
    """Generate dashboard metrics and reports"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_overview_metrics(self, period_days: int = 30) -> Dict:
        """Get overall business metrics"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=period_days)
        
        analytics = self.db.query(ProductAnalytics).filter(
            ProductAnalytics.date >= cutoff_date
        ).all()
        
        total_revenue = sum([a.revenue for a in analytics])
        total_sales = sum([a.sales for a in analytics])
        total_ad_spend = sum([a.ad_spend for a in analytics])
        
        active_products = self.db.query(Product).filter(
            Product.status == "active"
        ).count()
        
        avg_order_value = total_revenue / total_sales if total_sales > 0 else 0
        
        return {
            "period_days": period_days,
            "total_revenue": round(total_revenue, 2),
            "total_sales": total_sales,
            "total_ad_spend": round(total_ad_spend, 2),
            "net_profit": round(total_revenue - total_ad_spend, 2),
            "active_products": active_products,
            "average_order_value": round(avg_order_value, 2),
            "roi": round(((total_revenue - total_ad_spend) / total_ad_spend * 100), 2) if total_ad_spend > 0 else 0
        }
