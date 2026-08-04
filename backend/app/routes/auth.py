from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session


from app.schemas.user import UserCreate, UserLogin

from app.schemas.response import (
    UserCreatedResponse,
    LoginResponse
)

from app.database.database import get_db

from app.models.user import User

from app.utils.security import (
    hash_password,
    verify_password
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post(
    "/signup",
    response_model=UserCreatedResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):


    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )



    new_user = User(

        username=user.username,

        email=user.email,

        password_hash=hash_password(
            user.password
        )
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)



    return {

        "message": "User created successfully",

        "user": {

            "username": new_user.username,

            "email": new_user.email

        }
    }




@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):


    existing_user = (

        db.query(User)

        .filter(
            User.email == user.email
        )

        .first()
    )


    if not existing_user:

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )


    if not verify_password(

        user.password,

        existing_user.password_hash

    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )



    return {

        "message": "Login successful",

        "user": {

            "username": existing_user.username,

            "email": existing_user.email

        }
    }