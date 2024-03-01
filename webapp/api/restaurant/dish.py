from typing import List

from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.restaurant.router import dish_router
from webapp.crud.dish import create_dish, delete_dish, get_dish, get_dishes, update_dish
from webapp.db.postgres import get_session
from webapp.models.sirius.dish import DishCategory
from webapp.schema.restaurant.dish import DishCreate, DishRead, DishUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@dish_router.post('/', response_model=DishRead, tags=['Dishes'])
async def create_dish_endpoint(
    dish_data: DishCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] is ['Администратор', 'Сотрудник']:
        try:
            return await create_dish(session=session, dish_data=dish_data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@dish_router.get('/{dish_id}', response_model=DishRead, tags=['Dishes'])
async def get_dish_endpoint(dish_id: int, session: AsyncSession = Depends(get_session)):
    try:
        dish = await get_dish(session=session, dish_id=dish_id)
        if dish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
        return dish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@dish_router.get('/', response_model=List[DishRead], tags=['Dishes'])
async def get_dishes_endpoint(
    session: AsyncSession = Depends(get_session),
    category: DishCategory = Query(None, description='Фильтр по категории блюд'),
):
    try:
        return await get_dishes(session=session, category=category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@dish_router.put('/{dish_id}', response_model=DishRead, tags=['Dishes'])
async def update_dish_endpoint(
    dish_id: int,
    dish_data: DishUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] is ['Администратор', 'Сотрудник']:
        try:
            dish = await update_dish(session=session, dish_id=dish_id, dish_data=dish_data)
            if dish is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return dish
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@dish_router.delete('/{dish_id}', response_model=int, tags=['Dishes'])
async def delete_dish_endpoint(
    dish_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] is ['Администратор', 'Сотрудник']:
        try:
            deleted_dish_id = await delete_dish(session=session, dish_id=dish_id)
            if deleted_dish_id == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return deleted_dish_id
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
