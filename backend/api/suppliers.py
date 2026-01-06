from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.models import Supplier
from backend.models.schemas import SupplierCreate, SupplierResponse

router = APIRouter()

@router.post("/", response_model=SupplierResponse)
async def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """Create a new supplier"""
    db_supplier = Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.get("/", response_model=List[SupplierResponse])
async def list_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all suppliers"""
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Get a specific supplier"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.post("/{supplier_id}/update-score")
async def update_supplier_score(supplier_id: int, db: Session = Depends(get_db)):
    """Update supplier reliability score"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Calculate reliability score
    review_score = (supplier.positive_reviews / supplier.total_reviews * 100) if supplier.total_reviews > 0 else 0
    quality_weight = 0.4
    communication_weight = 0.3
    review_weight = 0.3
    
    reliability_score = (
        supplier.product_quality_score * quality_weight +
        supplier.communication_score * communication_weight +
        review_score * review_weight
    )
    
    supplier.reliability_score = round(reliability_score, 2)
    db.commit()
    db.refresh(supplier)
    
    return {"reliability_score": supplier.reliability_score}
