from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import user_router
from webapp.crud.user import create_user, get_user_by_id, update_user
from webapp.db.postgres import get_session
from webapp.schema.login.user import UserCreate, UserRead, UserUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.post(
    '/signup',
    response_model=UserRead,
    tags=['Users'],
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await create_user(session=session, user_data=user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get('/me', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def get_me_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        print('role: ', current_user['role'])
        user = await get_user_by_id(session=session, user_id=current_user['user_id'])
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.put('/me/update', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def update_user_endpoint(
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        user = await update_user(session=session, user_id=current_user['user_id'], user_data=user_data)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
