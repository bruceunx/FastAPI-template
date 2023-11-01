from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str


class CreateProductSchema(ProductBaseSchema):
    pass


class UpdateProductSchema(ProductBaseSchema):
    pass
