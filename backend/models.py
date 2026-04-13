import enum
from sqlalchemy import Column, Integer, String, Float, Date, Enum, Text
from backend.database import Base


class StatusEnum(str, enum.Enum):
    pantry = "Pantry"
    waste = "Waste"
    consumed = "Consumed"


class FoodItem(Base):
    """
    SQLAlchemy model for the FoodItem table.
    Tracks food from farm origin all the way through consumption or disposal.
    """
    __tablename__ = "food_items"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name        = Column(String(100),  nullable=False, index=True)
    batch_id    = Column(String(50),   nullable=False, unique=True, index=True)
    origin_farm = Column(String(150),  nullable=False)
    harvest_date = Column(Date,        nullable=False)
    expiry_date  = Column(Date,        nullable=False)
    calories    = Column(Float,        nullable=True)   # kcal per 100 g
    sugar       = Column(Float,        nullable=True)   # grams per 100 g
    allergens   = Column(Text,         nullable=True)   # comma-separated list e.g. "Gluten, Nuts"
    status      = Column(
        Enum(StatusEnum, values_callable=lambda e: [i.value for i in e]),
        nullable=False,
        default=StatusEnum.pantry
    )
