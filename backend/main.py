from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.database import engine, get_db
from backend import models

# ── Bootstrap DB ──────────────────────────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AgriLoop Food Management API",
    description=(
        "CRUD backend for managing food items from farm to table. "
        "Track batch origin, nutritional data, allergens, and lifecycle status."
    ),
    version="1.0.0",
)

# ── CORS (allows the frontend HTML to call this API) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes: Food Items ────────────────────────────────────────────────────────

@app.post(
    "/food-items",
    response_model=schemas.FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new food item",
    tags=["Food Items"],
)
def create_item(payload: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    """
    Add a new food item to the database.  
    `batch_id` must be unique across all records.
    """
    try:
        return crud.create_food_item(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A food item with batch_id='{payload.batch_id}' already exists.",
        )


@app.get(
    "/food-items",
    response_model=List[schemas.FoodItemResponse],
    summary="List all food items",
    tags=["Food Items"],
)
def list_items(
    skip: int = Query(0, ge=0, description="Records to skip (pagination)"),
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    status_filter: Optional[models.StatusEnum] = Query(None, alias="status", description="Filter by status"),
    db: Session = Depends(get_db),
):
    """
    Retrieve all food items.  
    Optionally filter by **status**: `Pantry`, `Waste`, or `Consumed`.
    """
    return crud.get_food_items(db, skip=skip, limit=limit, status=status_filter)


@app.get(
    "/food-items/{item_id}",
    response_model=schemas.FoodItemResponse,
    summary="Get a single food item",
    tags=["Food Items"],
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Fetch a single food item by its **ID**."""
    item = crud.get_food_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id={item_id} not found.",
        )
    return item


@app.patch(
    "/food-items/{item_id}",
    response_model=schemas.FoodItemResponse,
    summary="Partially update a food item",
    tags=["Food Items"],
)
def update_item(
    item_id: int,
    payload: schemas.FoodItemUpdate,
    db: Session = Depends(get_db),
):
    """
    Update one or more fields of an existing food item.  
    Only the fields included in the request body are modified.
    """
    item = crud.update_food_item(db, item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id={item_id} not found.",
        )
    return item


@app.delete(
    "/food-items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a food item",
    tags=["Food Items"],
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Permanently delete a food item by its **ID**."""
    deleted = crud.delete_food_item(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id={item_id} not found.",
        )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "app": "AgriLoop API v1.0.0"}
