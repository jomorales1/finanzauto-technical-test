from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    quantity: int
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )


class ProductUpdate(SQLModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None