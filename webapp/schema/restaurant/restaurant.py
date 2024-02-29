from typing import List, Optional

from pydantic import BaseModel


# Основная модель
class RestaurantSchema(BaseModel):
    id: int
    name: str
    address: str
    description: str
    menu: List[int]


# Модель для создания
class RestaurantCreate(BaseModel):
    name: str
    address: str
    description: str
    menu: List[int]


# Модель для обновления
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    menu: Optional[List[int]] = None
