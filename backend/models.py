from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator

class InventoryItem(BaseModel):
    item_name: str = Field(..., description="The specific name of the product or item.")
    category: Literal['Groceries', 'Electronics', 'Office Supplies', 'Furniture', 'Other'] = Field(
        default='Other', description="Broad category of the item."
    )
    quantity: float = Field(..., gt=0, description="Count or weight of the item.")
    unit: str = Field(default="pcs", description="Unit of measure (e.g., kg, lbs, pcs, box).")
    unit_price: Optional[float] = Field(None, description="Price per unit if visible.")
    total_price: Optional[float] = Field(None, description="Total price for this line item.")
    
    @field_validator('item_name')
    def clean_name(cls, v):
        return v.strip().title()

class InventoryExtractionResult(BaseModel):
    items: List[InventoryItem]
    merchant_name: Optional[str] = Field(None, description="Name of the store or location if visible.")
    scan_date: Optional[str] = Field(None, description="Date visible on the receipt/image (ISO format).")
    confidence_score: float = Field(
        ..., ge=0, le=1, 
        description="A self-assessed confidence score (0.0 to 1.0) regarding the legibility and accuracy of extraction."
    )
