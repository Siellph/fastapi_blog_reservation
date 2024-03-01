from typing import List

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.restaurant.router import restaurant_router
from webapp.crud.dish import get_dishes_by_restaurant_id_and_category
from webapp.crud.restaurant import (
    create_restaurant,
    delete_restaurant,
    get_restaurant,
    get_restaurants,
    update_restaurant,
)
from webapp.db.postgres import get_session
from webapp.models.sirius.dish import DishCategory
from webapp.schema.restaurant.dish import DishRead
from webapp.schema.restaurant.restaurant import RestaurantCreate, RestaurantRead, RestaurantUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@restaurant_router.post('/', response_model=RestaurantRead, tags=['Restaurants'], status_code=status.HTTP_201_CREATED)
async def create_new_restaurant(
    restaurant_data: RestaurantCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'Администратор':
        try:
            return await create_restaurant(session=session, restaurant_data=restaurant_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@restaurant_router.get('/{restaurant_id}', response_model=RestaurantRead, tags=['Restaurants'])
async def get_single_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        restaurant = await get_restaurant(session=session, restaurant_id=restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
        return restaurant
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@restaurant_router.get('/{restaurant_id}/menu', response_model=List[DishRead], tags=['Restaurants'])
async def get_dishes_for_restaurant(
    restaurant_id: int,
    category: DishCategory = Query(None, description='Фильтр по категории блюд'),
    session: AsyncSession = Depends(get_session),
):
    try:
        dishes = await get_dishes_by_restaurant_id_and_category(
            session=session, restaurant_id=restaurant_id, category=category
        )
        if not dishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
        return dishes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@restaurant_router.get('/', response_model=List[RestaurantRead], tags=['Restaurants'])
async def get_all_restaurants(session: AsyncSession = Depends(get_session)):
    try:
        return await get_restaurants(session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@restaurant_router.put('/{restaurant_id}', response_model=RestaurantRead, tags=['Restaurants'])
async def update_existing_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'Администратор':
        try:
            restaurant = await update_restaurant(
                session=session, restaurant_id=restaurant_id, restaurant_data=restaurant_data
            )
            if not restaurant:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return restaurant
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@restaurant_router.delete('/{restaurant_id}', response_model=int, tags=['Restaurants'])
async def delete_existing_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'Администратор':
        try:
            deleted_restaurant_id = await delete_restaurant(session=session, restaurant_id=restaurant_id)
            if not deleted_restaurant_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return deleted_restaurant_id
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
