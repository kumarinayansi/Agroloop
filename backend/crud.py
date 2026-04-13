from typing import List, Optional
from sqlalchemy.orm import Session
from backend import models, schemas


# ── CREATE ────────────────────────────────────────────────────────────────────
def create_food_item(db: Session, payload: schemas.FoodItemCreate) -> models.FoodItem:
    db_item = models.FoodItem(**payload.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ── READ (single) ─────────────────────────────────────────────────────────────
def get_food_item(db: Session, item_id: int) -> Optional[models.FoodItem]:
    return db.query(models.FoodItem).filter(models.FoodItem.id == item_id).first()


# ── READ (all, with optional filters) ────────────────────────────────────────
def get_food_items(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[models.StatusEnum] = None,
) -> List[models.FoodItem]:
    query = db.query(models.FoodItem)
    if status:
        query = query.filter(models.FoodItem.status == status)
    return query.offset(skip).limit(limit).all()


# ── UPDATE (partial) ──────────────────────────────────────────────────────────
def update_food_item(
    db: Session,
    item_id: int,
    payload: schemas.FoodItemUpdate,
) -> Optional[models.FoodItem]:
    db_item = get_food_item(db, item_id)
    if not db_item:
        return None
    # Only apply fields that were explicitly provided
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


# ── DELETE ────────────────────────────────────────────────────────────────────
def delete_food_item(db: Session, item_id: int) -> bool:
    db_item = get_food_item(db, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True
