from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas import Token, UserBase, UserToCreate

from api.utils import authenticate_user, create_access_token, get_current_active_user, create_user


router = APIRouter(tags=["registration"])


@router.post("/sing-up", response_model=UserBase)
async def registrate_user(user: UserToCreate):
    return await create_user(user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(weeks=1)
    access_token = await create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_active_user)]):
    return current_user
