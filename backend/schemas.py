from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from backend.models import StatusEnum


# ── Shared base ──────────────────────────────────────────────────────────────
class FoodItemBase(BaseModel):
    model_config = {"json_schema_extra": {"example": {
        "name": "Organic Tomatoes",
        "batch_id": "BATCH-2024-001",
        "origin_farm": "Green Valley Farm, Karnataka",
        "harvest_date": "2024-04-01",
        "expiry_date": "2024-04-15",
        "calories": 18.0,
        "sugar": 2.6,
        "allergens": "None",
        "status": "Pantry",
    }}}

    name:         str   = Field(..., min_length=1, max_length=100)
    batch_id:     str   = Field(...)
    origin_farm:  str   = Field(...)
    harvest_date: date
    expiry_date:  date
    calories:     Optional[float] = Field(None, ge=0, description="kcal per 100g")
    sugar:        Optional[float] = Field(None, ge=0, description="grams per 100g")
    allergens:    Optional[str]   = None
    status:       StatusEnum      = StatusEnum.pantry


# ── Create: all fields required from the client ───────────────────────────────
class FoodItemCreate(FoodItemBase):
    pass


# ── Update: every field is optional (PATCH semantics) ─────────────────────────
class FoodItemUpdate(BaseModel):
    name:         Optional[str]        = Field(None, min_length=1, max_length=100)
    batch_id:     Optional[str]        = None
    origin_farm:  Optional[str]        = None
    harvest_date: Optional[date]       = None
    expiry_date:  Optional[date]       = None
    calories:     Optional[float]      = Field(None, ge=0)
    sugar:        Optional[float]      = Field(None, ge=0)
    allergens:    Optional[str]        = None
    status:       Optional[StatusEnum] = None


# ── Read / Response: same as base + server-generated id ───────────────────────
class FoodItemResponse(FoodItemBase):
    id: int

    class Config:
        from_attributes = True  # ORM-mode for Pydantic v2
