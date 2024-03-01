from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.restaurant.router import reservation_router
from webapp.crud.reservation import (
    create_reservation,
    delete_reservation,
    get_reservation,
    get_reservations,
    update_reservation,
)
from webapp.db.postgres import get_session
from webapp.schema.reservation.reservation import ReservationCreate, ReservationRead, ReservationUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@reservation_router.post('/', response_model=ReservationRead, tags=['Reservations'], response_class=ORJSONResponse)
async def create_reservation_endpoint(
    reservation_data: ReservationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        return await create_reservation(session=session, reservation_data=reservation_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@reservation_router.get(
    '/{reservation_id}',
    response_model=ReservationRead,
    tags=['Reservations'],
    response_class=ORJSONResponse,
)
async def read_reservation_endpoint(reservation_id: int, session: AsyncSession = Depends(get_session)):
    try:
        reservation = await get_reservation(session=session, reservation_id=reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
        return reservation
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@reservation_router.get('/', response_model=list[ReservationRead], tags=['Reservations'], response_class=ORJSONResponse)
async def read_reservations_endpoint(session: AsyncSession = Depends(get_session)):
    try:
        return await get_reservations(session=session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@reservation_router.put(
    '/{reservation_id}',
    response_model=ReservationRead,
    tags=['Reservations'],
    response_class=ORJSONResponse,
)
async def update_reservation_endpoint(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'Сотрудник':
        try:
            reservation = await update_reservation(
                session=session, reservation_id=reservation_id, reservation_data=reservation_data
            )
            if not reservation:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return reservation
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')


@reservation_router.delete(
    '/{reservation_id}', response_model=dict, tags=['Reservations'], response_class=ORJSONResponse
)
async def delete_reservation_endpoint(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'Сотрудник':
        try:
            deleted_reservation_id = await delete_reservation(session=session, reservation_id=reservation_id)
            if not deleted_reservation_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')
            return {'message': f'Резерв {deleted_reservation_id} отменен.'}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
