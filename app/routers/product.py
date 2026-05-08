import json

from fastapi import APIRouter, Depends, HTTPException
from redis.exceptions import RedisError
from sqlalchemy.orm import Session

from app.models import Product, ProductCreate
from app.database import get_db
from app import crud
from app.redis_client import redis_client
from app.utils.security import verify_token


router = APIRouter()
CACHE_TTL_SECONDS = 60


def product_to_dict(product):
    return Product.model_validate(product).model_dump()


def products_to_list(products):
    return [product_to_dict(product) for product in products]


def get_cached_data(cache_key: str):
    try:
        cached_data = redis_client.get(cache_key)
    except RedisError:
        return None

    if cached_data:
        return json.loads(cached_data)

    return None


def set_cached_data(cache_key: str, data):
    try:
        redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(data))
    except RedisError:
        pass


@router.get("/product")
def get_all_products(current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    cache_key = "products:all"
    cached_products = get_cached_data(cache_key)

    if cached_products is not None:
        return cached_products

    products = products_to_list(crud.get_all(db))
    set_cached_data(cache_key, products)

    return products


@router.post("/product")
def add_product(product: ProductCreate, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):

    if product.price <= 0:
        raise HTTPException(400, "Price must be greater than zero")

    if product.quantity < 0:
        raise HTTPException(400, "Quantity cannot be negative")

    return crud.create(db, product)


@router.put("/product/{id}")
def update_product(id: int, product: ProductCreate, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):

    db_product = crud.get_by_id(db, id)

    if not db_product:
        raise HTTPException(404, "Product not found")

    if product.price <= 0:
        raise HTTPException(400, "Price must be greater than zero")

    if product.quantity < 0:
        raise HTTPException(400, "Quantity cannot be negative")

    return crud.update(db, db_product, product)


@router.delete("/product/{id}")
def delete_product(id: int, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):

    db_product = crud.get_by_id(db, id)

    if not db_product:
        raise HTTPException(404, "Product not found")

    crud.delete(db, db_product)

    return {"message": "Product deleted successfully"}


@router.get("/product/search/{name}")
def search(name: str, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    cache_key = f"products:search:name:{name.lower()}"
    cached_products = get_cached_data(cache_key)

    if cached_products is not None:
        return cached_products

    products = products_to_list(crud.search_by_name(db, name))
    set_cached_data(cache_key, products)

    return products


@router.get("/product/page/")
def get_by_page(page: int = 1, limit: int = 5, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    cache_key = f"products:page:{page}:limit:{limit}"
    cached_products = get_cached_data(cache_key)

    if cached_products is not None:
        return cached_products

    products = products_to_list(crud.pagination(db, page, limit))
    set_cached_data(cache_key, products)

    return products


@router.get("/product/price/")
def price_filter(min_price: float, current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    cache_key = f"products:price:min:{min_price}"
    cached_products = get_cached_data(cache_key)

    if cached_products is not None:
        return cached_products

    products = products_to_list(crud.filter_by_price(db, min_price))
    set_cached_data(cache_key, products)

    return products


@router.get("/product/{id}")
def get_product_by_id(id: int,current_user: str = Depends(verify_token), db: Session = Depends(get_db)):
    cache_key = f"products:id:{id}"
    cached_product = get_cached_data(cache_key)

    if cached_product is not None:
        return cached_product

    db_product = crud.get_by_id(db, id)

    if not db_product:
        raise HTTPException(404, "Product not found")

    product = product_to_dict(db_product)
    set_cached_data(cache_key, product)

    return product
