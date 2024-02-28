import enum
from typing import TYPE_CHECKING, List

from sqlalchemy import Float, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.restaurant import Restaurant


class DishCategory(str, enum.Enum):
    APPETIZER = 'Закуска'
    MAIN_COURSE = 'Основное блюдо'
    DESSERT = 'Десерт'
    SOUP = 'Суп'
    SALAD = 'Салат'
    HOT_DRINK = 'Горячий напиток'
    COLD_DRINK = 'Холодный напиток'


DishCategoryType: ENUM = ENUM(
    DishCategory,
    name='dish_category',
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class Dish(Base):
    __tablename__ = 'dish'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id: Mapped[List['Restaurant']] = relationship(
        'Restaurant',
        secondary=f'{DEFAULT_SCHEMA}.restaurant_dish',
        back_populates='menu',
    )
    category: Mapped[ENUM] = mapped_column(DishCategoryType)
    dish_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float(precision=2))
