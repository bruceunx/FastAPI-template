from typing import Annotated

from fastapi import APIRouter, Depends, Request

from schemas.products import CreateProductSchema, UpdateProductSchema  # type: ignore
from auth.auth_handler import get_current_user, get_rol_user
from services.products import create_product, delete_single_product, get_batch_products, get_single_product, update_single_product  # type: ignore
from services.users import create_logger

router = APIRouter()

DEFAULT_PAGE = 1
MAX_PAGE_SIZE = 100


@router.post("/product", status_code=201)
async def upload_product(
    request: Request,
    product: CreateProductSchema,
    current_user: Annotated[
        str,
        Depends(get_rol_user),
    ],
):
    host = request.client.host
    await create_logger(current_user, host)

    record_id = await create_product(product)
    return {"id": record_id, **product.dict()}


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    current_user: Annotated[
        str,
        Depends(get_current_user),
    ],
):
    product = await get_single_product(product_id)
    return product


@router.get("/products/")
async def get_products(
    current_user: Annotated[
        str,
        Depends(get_current_user),
    ],
    page: int = 1,
    limit: int = 10,
):
    page = max(page, DEFAULT_PAGE)
    page_size = min(limit, MAX_PAGE_SIZE)
    total_num, products = await get_batch_products(page, page_size)
    return {"total_num": total_num, "products": products}


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    product: UpdateProductSchema,
    current_user: Annotated[
        str,
        Depends(get_current_user),
    ],
):

    try:
        product = await update_single_product(product_id, product)
    except Exception:
        return {"error": "cannot process the action"}
    if product is None:
        return {"error": "product is wrong"}
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: Annotated[
        str,
        Depends(get_current_user),
    ],
):
    ret = await delete_single_product(product_id)
    if ret:
        return {"success": f"product_id:{product_id} is deleted successfully"}
    else:
        return {"error": "cannot handle the delete action"}
