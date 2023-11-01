from sqlalchemy import delete, desc, insert, select, func, update

from db import DB
from models.products import Product  # type: ignore
from schemas.products import CreateProductSchema, UpdateProductSchema  # type: ignore


async def create_product(product: CreateProductSchema):
    query = insert(Product)
    return await DB.execute(query, values={"name": product.name})


async def get_single_product(id: int) -> Product | None:
    query = select(Product).where(Product.id == id)
    return await DB.fetch_one(query=query)


async def get_batch_products(page: int,
                             page_size: int) -> tuple[int, list[Product]]:
    total_query = select([func.count()]).select_from(Product)
    total_count = await DB.fetch_val(total_query)
    start_idx = (page - 1) * page_size
    query = select(Product).order_by(desc(
        Product.id)).offset(start_idx).limit(page_size)
    products = await DB.fetch_all(query)
    return total_count, products


async def update_single_product(product_id: int, product: UpdateProductSchema):
    query = update(Product).where(Product.id == product_id)
    await DB.execute(query, values={"name": product.name})
    query = select(Product).where(Product.id == product_id)
    return await DB.fetch_one(query)


async def delete_single_product(id: int):
    query = delete(Product).where(Product.id == id)
    return await DB.execute(query)
