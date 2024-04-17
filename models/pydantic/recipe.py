from typing import Optional
from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str = None
    making_time: str = None
    serves: str = None
    ingredients: str = None
    cost: int = None

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None
