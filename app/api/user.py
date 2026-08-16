from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.auth.sec import hash_password
from ..database import get_db
from ..schema import UserCreate,UserOut,UserLogin
from ..auth import hash_password,verify
from ..models import User


router=APIRouter(prefix="/user")

@router.post("/create",response_model=UserOut)
def create_user(user:UserCreate,db:Session=Depends(get_db())):
    hashed_password=hash_password(user.password)
    new_user=User(name=user.name,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user_cred:UserLogin,db:Session=Depends(get_db())):
    user=db.query(User).filter(User.email==user_cred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid Credentials")
    if not verify(user_cred.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentils"
        )
    