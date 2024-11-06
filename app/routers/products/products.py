from fastapi import APIRouter, Depends, HTTPException, Query
from app.routers.products.models import Product, ProductUpdate
from app.helpers import products
from app.routers.auth import auth
from app.utilities.cache import cache
from app.utilities.logger import logger

import json


router = APIRouter()

@router.get("")
async def get_products(page: int = Query(default=1, gt=0), limit: int = Query(default=10, le=100), redis_client=Depends(cache)):
    if cached_response := redis_client.get(f"products:{page}:{limit}"):
        logger.info(f"Cache hit for products:{page}:{limit}")
        return json.loads(cached_response)
    products_list = products.get_products(page, limit)
    redis_client.set(f"products:{page}:{limit}", json.dumps([product.model_dump() for product in products_list], default=str), ex=30)
    return products_list

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