from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.database import get_db
from models.models import Product
from models.schemas import ProductCreate, ProductResponse
from services.product_research.trend_analyzer import ProfitCalculator

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    calculator = ProfitCalculator()
    margins = calculator.calculate_margins(product.cost, product.price)
    
    db_product = Product(
        **product.model_dump(),
        profit_margin=margins["net_margin_percent"]
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductResponse])
async def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all products"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    calculator = ProfitCalculator()
    margins = calculator.calculate_margins(product.cost, product.price)
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db_product.profit_margin = margins["net_margin_percent"]
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/{product_id}/calculate-profit")
async def calculate_profit(product_id: int, ad_spend: float = 0, db: Session = Depends(get_db)):
    """Calculate profit for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    calculator = ProfitCalculator()
    return calculator.calculate_margins(product.cost, product.price, ad_spend)
