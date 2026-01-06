#!/usr/bin/env python3
"""
Admin API - Handle admin panel settings and control AI systems
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime

router = APIRouter()

class AdminSettings(BaseModel):
    scanFrequency: int = 60
    profitMargin: int = 30
    maxPrice: int = 100
    contentQuality: int = 2
    postFrequency: int = 3
    stockThreshold: int = 20
    autoFinder: bool = True
    autoPost: bool = False
    autoRestock: bool = False
    timestamp: Optional[str] = None

# Settings file path
SETTINGS_FILE = "admin_settings.json"

@router.post("/api/admin/settings")
async def save_settings(settings: AdminSettings):
    """Save admin settings"""
    try:
        settings_dict = settings.dict()
        settings_dict['timestamp'] = datetime.now().isoformat()
        
        # Save to file
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings_dict, f, indent=2)
        
        # Apply settings to running systems
        apply_settings(settings_dict)
        
        return {
            "success": True,
            "message": "Settings saved and applied",
            "settings": settings_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/admin/settings")
async def get_settings():
    """Get current admin settings"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            return {"success": True, "settings": settings}
        else:
            # Return defaults
            return {
                "success": True,
                "settings": AdminSettings().dict()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def apply_settings(settings: dict):
    """Apply settings to running AI systems"""
    
    # Update .env file with new settings
    env_updates = {
        'SCAN_FREQUENCY_MINUTES': str(settings['scanFrequency']),
        'MIN_PROFIT_MARGIN': str(settings['profitMargin']),
        'MAX_PRODUCT_PRICE': str(settings['maxPrice']),
        'CONTENT_QUALITY_LEVEL': str(settings['contentQuality']),
        'SOCIAL_POST_FREQUENCY': str(settings['postFrequency']),
        'STOCK_ALERT_THRESHOLD': str(settings['stockThreshold']),
        'AUTO_FINDER_ENABLED': str(settings['autoFinder']),
        'AUTO_POST_ENABLED': str(settings['autoPost']),
        'AUTO_RESTOCK_ENABLED': str(settings['autoRestock'])
    }
    
    # Update environment variables
    for key, value in env_updates.items():
        os.environ[key] = value
    
    # Write to .env file
    update_env_file(env_updates)
    
    print(f"✅ Applied settings: {settings}")

def update_env_file(updates: dict):
    """Update .env file with new values"""
    env_path = '.env'
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Update existing or add new
    updated_keys = set()
    new_lines = []
    
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            key = line.split('=')[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add new keys
    for key, value in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(new_lines)

# Export router
admin_router = router
