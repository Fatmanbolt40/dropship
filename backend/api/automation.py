from fastapi import APIRouter
from backend.services.store_automation.shopify_integration import (
    ShopifyIntegration,
    ProductOptimizer,
    AutomationRules
)

router = APIRouter()

@router.post("/shopify/import-product")
async def import_to_shopify(product_data: dict):
    """Import product to Shopify with AI-generated content"""
    integration = ShopifyIntegration()
    # integration.connect()  # Uncomment when credentials are configured
    result = await integration.import_product(product_data)
    return result

@router.post("/shopify/update-pricing")
async def update_pricing(product_id: str, new_price: float, strategy: str = "competitive"):
    """Update product pricing with strategy"""
    integration = ShopifyIntegration()
    return await integration.update_pricing(product_id, new_price, strategy)

@router.post("/shopify/sync-inventory")
async def sync_inventory(product_id: str, quantity: int):
    """Sync inventory across platforms"""
    integration = ShopifyIntegration()
    return await integration.sync_inventory(product_id, quantity)

@router.post("/optimize/seo")
async def optimize_seo(product_data: dict):
    """Optimize product for SEO"""
    optimizer = ProductOptimizer()
    return await optimizer.optimize_seo(product_data)

@router.post("/optimize/images")
async def enhance_images(image_urls: list[str]):
    """Get image enhancement recommendations"""
    optimizer = ProductOptimizer()
    return await optimizer.enhance_images(image_urls)

@router.post("/automation/price-rule")
async def create_price_rule(product_id: str, condition: dict, action: dict):
    """Create automated price adjustment rule"""
    automation = AutomationRules()
    return automation.create_price_adjustment_rule(product_id, condition, action)

@router.post("/automation/inventory-alert")
async def create_inventory_alert(product_id: str, threshold: int = 10):
    """Create low inventory alert"""
    automation = AutomationRules()
    return automation.create_inventory_alert_rule(product_id, threshold)

@router.post("/automation/performance-pause")
async def create_performance_pause(product_id: str, min_roi: float = 100):
    """Create rule to pause underperforming products"""
    automation = AutomationRules()
    return automation.create_performance_pause_rule(product_id, min_roi)

@router.get("/automation/rules")
async def get_automation_rules():
    """Get all automation rules"""
    automation = AutomationRules()
    return {"rules": automation.get_all_rules()}
