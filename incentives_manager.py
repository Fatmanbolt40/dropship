"""
Amazon New Seller Incentives AI Manager
Automatically tracks and optimizes for $50K+ in Amazon seller incentives
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

class IncentivesManager:
    def __init__(self):
        self.config_file = "incentives_config.json"
        self.load_config()
        
    def load_config(self):
        """Load incentives configuration"""
        with open(self.config_file, 'r') as f:
            data = json.load(f)
            self.config = data['amazon_new_seller_incentives']
    
    def save_config(self):
        """Save incentives configuration"""
        with open(self.config_file, 'w') as f:
            json.dump({'amazon_new_seller_incentives': self.config}, f, indent=2)
    
    def initialize_seller_account(self):
        """Initialize when seller account is created"""
        self.config['enrollment_date'] = datetime.now().isoformat()
        self.config['day_90_deadline'] = (datetime.now() + timedelta(days=90)).isoformat()
        self.save_config()
        return {
            "message": "New Seller Incentives tracking initialized!",
            "potential_value": "$50,000+",
            "deadline": self.config['day_90_deadline']
        }
    
    def get_pending_actions(self) -> List[Dict]:
        """Get prioritized list of actions to take"""
        actions = []
        now = datetime.now()
        
        # Brand Registry (highest priority - unlocks most benefits)
        if not self.config['brand_registry_enrolled']:
            actions.append({
                "priority": 1,
                "action": "Enroll in Amazon Brand Registry",
                "value": "$5,000+ in bonuses + $200 Vine credit",
                "deadline_days": 180,
                "unlocks": ["10% sales bonus", "Vine", "A+ Content", "Sponsored Brands"]
            })
        
        # FBA Setup (critical for fulfillment incentives)
        if not self.config['required_services']['fulfillment_by_amazon']['enabled']:
            actions.append({
                "priority": 2,
                "action": "Enable Fulfillment by Amazon (FBA)",
                "value": "$700 in credits + free storage/returns",
                "deadline_days": 90,
                "benefits": ["$100 partnered carrier", "$200 AGL", "$400 inbound placement"]
            })
        
        # Sponsored Products (easy wins)
        if not self.config['advertising_goals']['sponsored_products_tier_1']['campaign_created']:
            actions.append({
                "priority": 3,
                "action": "Create Sponsored Products campaign",
                "value": "Up to $1,250 in ad credits",
                "deadline_days": 90,
                "tiers": ["$50→$50", "$200→$200", "$1000→$1000"]
            })
        
        # Automate Pricing
        if not self.config['required_services']['automate_pricing']['enabled']:
            actions.append({
                "priority": 4,
                "action": "Enable Automate Pricing",
                "value": "Required for New Seller Guide",
                "deadline_days": 90
            })
        
        # Coupons
        if not self.config['advertising_goals']['coupons']['status'] == 'completed':
            actions.append({
                "priority": 5,
                "action": "Create Amazon Coupon",
                "value": "$50 credit",
                "deadline_days": 90
            })
        
        return sorted(actions, key=lambda x: x['priority'])
    
    def check_product_eligibility(self, product: Dict) -> Dict:
        """Check if product is eligible for incentives"""
        eligible_for = []
        recommendations = []
        
        # FBA eligibility
        if product.get('fulfillment_method') == 'FBA':
            eligible_for.append("FBA New Selection (free storage/returns)")
            eligible_for.append("Inbound Placement Credit ($400)")
        else:
            recommendations.append("Enable FBA to unlock $700+ in credits")
        
        # Brand Registry eligibility
        if product.get('brand_registered'):
            eligible_for.append("10% sales bonus (up to $5,000)")
            eligible_for.append("Vine enrollment ($200 credit)")
            eligible_for.append("A+ Content")
            eligible_for.append("Sponsored Brands ads")
        else:
            recommendations.append("Register brand for $5,000+ in bonuses")
        
        # Advertising eligibility
        if product.get('price', 0) > 0:
            eligible_for.append("Sponsored Products ($1,250 credits available)")
            eligible_for.append("Coupons ($50 credit)")
        
        return {
            "eligible_for": eligible_for,
            "recommendations": recommendations,
            "potential_value": self.calculate_product_incentive_value(product)
        }
    
    def calculate_product_incentive_value(self, product: Dict) -> float:
        """Calculate potential incentive value for a product"""
        total_value = 0
        
        # Brand Registry bonus (10% on first $50k in sales)
        if product.get('brand_registered'):
            estimated_annual_sales = product.get('estimated_sales', 0)
            if estimated_annual_sales > 0:
                bonus_sales = min(estimated_annual_sales, 50000)
                total_value += bonus_sales * 0.10
        
        # FBA credits
        if product.get('fulfillment_method') == 'FBA':
            total_value += 700  # Avg FBA incentive value
        
        # Advertising credits
        total_value += 50  # Coupon credit
        
        return round(total_value, 2)
    
    def track_branded_sale(self, sale_amount: float):
        """Track sale for Brand Registry bonus calculation"""
        if not self.config['brand_registry_enrolled']:
            return
        
        bonus_config = self.config['brand_registry_goals']['branded_sales_bonus']
        current_sales = bonus_config['sales_tracked']
        new_total = current_sales + sale_amount
        
        # Calculate bonus
        if new_total <= 50000:
            # Tier 1: 10% on first $50k
            bonus = sale_amount * 0.10
            bonus_config['tier_1']['earned'] += bonus
        elif current_sales < 50000 < new_total:
            # Split between tier 1 and tier 2
            tier_1_amount = 50000 - current_sales
            tier_2_amount = new_total - 50000
            bonus = (tier_1_amount * 0.10) + (tier_2_amount * 0.05)
            bonus_config['tier_1']['earned'] += tier_1_amount * 0.10
            bonus_config['tier_2']['earned'] += tier_2_amount * 0.05
        else:
            # Tier 2: 5% after $50k
            bonus = sale_amount * 0.05
            bonus_config['tier_2']['earned'] += bonus
        
        bonus_config['sales_tracked'] = new_total
        bonus_config['total_earned'] += bonus
        
        self.save_config()
        
        return {
            "sale_amount": sale_amount,
            "bonus_earned": round(bonus, 2),
            "total_bonus": round(bonus_config['total_earned'], 2),
            "progress": f"${new_total:,.2f} / $1,000,000"
        }
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics for admin panel"""
        total_credits_earned = 0
        total_credits_available = 0
        
        # Calculate earned and available credits
        for category in ['fba_goals', 'advertising_goals']:
            for goal, data in self.config[category].items():
                if isinstance(data, dict):
                    if data.get('status') == 'completed':
                        total_credits_earned += data.get('credit', 0)
                    elif data.get('status') == 'pending':
                        total_credits_available += data.get('credit', 0)
        
        # Add Brand Registry bonus
        brand_bonus = self.config['brand_registry_goals']['branded_sales_bonus']
        total_credits_earned += brand_bonus['total_earned']
        total_credits_available += (5000 - brand_bonus['tier_1']['earned']) + \
                                   (47500 - brand_bonus['tier_2']['earned'])
        
        return {
            "total_potential": 50000,
            "credits_earned": round(total_credits_earned, 2),
            "credits_available": round(total_credits_available, 2),
            "brand_registry_enrolled": self.config['brand_registry_enrolled'],
            "fba_enabled": self.config['required_services']['fulfillment_by_amazon']['enabled'],
            "days_remaining": self.get_days_remaining(),
            "completion_percentage": self.get_completion_percentage()
        }
    
    def get_days_remaining(self) -> int:
        """Get days remaining in 90-day window"""
        if not self.config.get('enrollment_date'):
            return 90
        
        enrolled = datetime.fromisoformat(self.config['enrollment_date'])
        deadline = enrolled + timedelta(days=90)
        remaining = (deadline - datetime.now()).days
        return max(0, remaining)
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage of required services"""
        required = self.config['required_services']
        total = len(required)
        completed = sum(1 for service in required.values() if service.get('enabled', False))
        return round((completed / total) * 100, 1)
    
    def generate_ai_strategy(self) -> Dict:
        """Generate AI strategy for maximizing incentives"""
        strategy = {
            "immediate_actions": [],
            "week_1_goals": [],
            "month_1_goals": [],
            "optimization_tips": []
        }
        
        # Immediate actions
        strategy["immediate_actions"] = [
            "Apply for Amazon Brand Registry (unlock $5,000+ in bonuses)",
            "Enable FBA for first products (unlock $700 in credits)",
            "Set up Automate Pricing tool",
            "Create first Sponsored Products campaign ($50 spend → $50 credit)"
        ]
        
        # Week 1 goals
        strategy["week_1_goals"] = [
            "Send first FBA shipment using Amazon Partnered Carrier ($100 credit)",
            "Create 5-10 product listings",
            "Enable dynamic pricing on all products",
            "Create first Amazon Coupon ($50 credit)"
        ]
        
        # Month 1 goals
        strategy["month_1_goals"] = [
            "Enroll products in Vine program ($200 credit)",
            "Scale Sponsored Products to $200 spend ($200 credit)",
            "Add A+ Content to branded products",
            "Create Sponsored Brands campaign",
            "Reach $5,000 in branded sales (earn $500 bonus)"
        ]
        
        # Optimization tips
        strategy["optimization_tips"] = [
            "Prioritize branded products for 10% sales bonus",
            "Use FBA for all products to maximize credits",
            "Create ads within 90 days to capture all ad credits",
            "Track branded sales to optimize for $1M bonus target",
            "Auto-enroll new products in FBA New Selection program"
        ]
        
        return strategy


# Global instance
incentives_manager = IncentivesManager()
