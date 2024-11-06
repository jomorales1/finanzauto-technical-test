from app.routers.products.models import Product, ProductUpdate
from app.utilities.db import engine
from sqlmodel import Session, select

def get_products(page: int = 1, limit: int = 10):
    with Session(engine) as session:
        statement = select(Product).offset((page - 1) * limit).limit(limit)
        products = session.exec(statement).all()
        return products

def get_product(id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()
        return product

def check_product_exists(id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()
        return product is not None

def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

def update_product(id: int, product: ProductUpdate):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product_db = session.exec(statement).first()
        product_data = product.model_dump(exclude_unset=True)
        product_db.sqlmodel_update(product_data)
        session.add(product_db)
        session.commit()
        session.refresh(product_db)
        return product_db

def delete_product(id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).first()
        session.delete(product)
        session.commit()
        return product