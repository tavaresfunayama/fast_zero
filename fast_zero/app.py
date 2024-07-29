from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserDb, UserList, UserPublic, UserSchema

app = FastAPI()
database = []


# @app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
# def create_user(user: UserSchema):
#     engine = create_engine(Settings().DATABASE_URL)

#     with Session(engine) as session:
#         db_user = session.scalar(
#             select(User).where(
#                 (User.username == user.username) | (User.email == user.email)
#             )
#         )

#         if db_user:
#             if db_user.username == user.username:
#                 raise HTTPException(
#                     status_code=HTTPStatus.BAD_REQUEST,
#                     detail='User already exists',
#                 )

#             elif db_user.email == user.email:
#                 raise HTTPException(
#                     status_code=HTTPStatus.BAD_REQUEST,
#                     detail='Email already exists',
#                 )

#         db_user = User(
#             username=user.username, email=user.email, password=user.password
#         )

#         session.add(db_user)
#         session.commit()
#         session.refresh(db_user)

#     return db_user

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDb(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
