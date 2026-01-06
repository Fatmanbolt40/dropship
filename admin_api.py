#!/usr/bin/env python3
"""
API Endpoint to trigger AI product finder
"""
from fastapi import APIRouter, BackgroundTasks
import subprocess
import os

router = APIRouter()

@router.post("/api/admin/run-ai-inventory")
async def run_ai_inventory(background_tasks: BackgroundTasks, count: int = 10):
    """Trigger AI inventory manager to find and add products"""
    
    def run_in_background():
        try:
            os.chdir('/home/Thalegendgamer/dropship')
            result = subprocess.run(
                ['./venv/bin/python', 'ai_inventory_manager.py'],
                capture_output=True,
                text=True,
                timeout=120
            )
            print(f"AI Inventory Manager output:\n{result.stdout}")
            if result.stderr:
                print(f"Errors:\n{result.stderr}")
        except Exception as e:
            print(f"Error running AI inventory: {e}")
    
    background_tasks.add_task(run_in_background)
    
    return {
        "success": True,
        "message": f"AI product finder started - will add up to {count} products",
        "status": "running"
    }

@router.post("/api/admin/clear-products")
async def clear_all_products():
    """Clear all products from campaigns directory"""
    try:
        import glob
        campaigns = glob.glob('/home/Thalegendgamer/dropship/campaigns/*.json')
        deleted = 0
        for campaign in campaigns:
            os.remove(campaign)
            deleted += 1
        
        return {
            "success": True,
            "message": f"Deleted {deleted} products",
            "count": deleted
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/api/admin/stats")
async def get_admin_stats():
    """Get comprehensive admin statistics"""
    try:
        import glob
        import json
        
        # Count products
        products = len(glob.glob('/home/Thalegendgamer/dropship/campaigns/*.json'))
        
        # Count orders and calculate totals
        orders = glob.glob('/home/Thalegendgamer/dropship/orders/*.json')
        total_revenue = 0
        total_profit = 0
        total_orders = len(orders)
        
        for order_file in orders:
            with open(order_file, 'r') as f:
                order = json.load(f)
                total_revenue += order.get('amount_paid', 0)
                total_profit += order.get('profit', 0)
        
        return {
            "products": products,
            "orders": total_orders,
            "revenue": round(total_revenue, 2),
            "profit": round(total_profit, 2),
            "avg_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
            "avg_profit_per_order": round(total_profit / total_orders, 2) if total_orders > 0 else 0
        }
    except Exception as e:
        return {
            "error": str(e),
            "products": 0,
            "orders": 0,
            "revenue": 0,
            "profit": 0
        }
