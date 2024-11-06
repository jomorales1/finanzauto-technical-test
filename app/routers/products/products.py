from fastapi import APIRouter, HTTPException
from app.routers.products.models import Product
from app.utilities.db import engine
from sqlmodel import Session, select


router = APIRouter()

@router.get("/products")
async def get_products():
    with Session(engine) as session:
        statement = select(Product)
        products = session.exec(statement)
        return products

@router.get("/products/{id}")
async def get_product(id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

@router.post("/products")
async def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

@router.put("/products/{id}")
async def update_product(id: int, product: Product):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product_db = session.exec(statement).first()
        if not product_db:
            raise HTTPException(status_code=404, detail="Product not found")
        product_db.name = product.name
        product_db.price = product.price
        product_db.quantity = product.quantity
        session.add(product_db)
        session.commit()
        session.refresh(product_db)
        return product_db

@router.delete("/products/{id}")
async def delete_product(id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return product