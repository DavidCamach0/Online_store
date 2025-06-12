from pydantic import BaseModel, Field
from typing import Annotated

class ItemCart(BaseModel):
    product_id: int
    quantity: Annotated[int, Field(gt=0)]
