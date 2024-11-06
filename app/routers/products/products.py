from fastapi import APIRouter, Depends, HTTPException, Query
from app.routers.products.models import Product, ProductUpdate
from app.helpers import products
from app.routers.auth import auth


router = APIRouter()

@router.get("")
async def get_products(page: int = Query(default=1, gt=0), limit: int = Query(default=10, le=100)):
    return products.get_products(page, limit)

@router.get("/{id}", dependencies=[Depends(auth.verify_token)])
async def get_product(id: int):
    product = products.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", dependencies=[Depends(auth.verify_token)], status_code=201)
async def create_product(product: Product):
    return products.create_product(product)

@router.put("/{id}", dependencies=[Depends(auth.verify_token)])
async def update_product(id: int, product: ProductUpdate):
    if not products.check_product_exists(id):
        raise HTTPException(status_code=404, detail="Product not found")
    return products.update_product(id, product)

@router.delete("/{id}", dependencies=[Depends(auth.verify_token)])
async def delete_product(id: int):
    if not products.check_product_exists(id):
        raise HTTPException(status_code=404, detail="Product not found")
    return products.delete_product(id)