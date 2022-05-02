from numpy import deprecate
from pydantic import BaseModel
import models
from typing import Optional
from fastapi import FastAPI,Depends,HTTPException,status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError


SECRET_KEY="BRO"
ALGORITHM="HS256"

"""
create a database if auth is called before main
"""

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

oauth2_bearer=OAuth2PasswordBearer(tokenUrl="token")

app=FastAPI()


class CreateUser(BaseModel):
    username:str
    email:Optional[str]
    first_name:str
    last_name:str
    password:str

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)

def authenticate_user(username:str,password:str,db):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:Optional[timedelta]=None):
    encode={"sub":username,"id":user_id}
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

"""
Tar inn en gylding token!
"""
async def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        user_id:int=payload.get("id")
        if username and user_id is None:
            raise get_user_exception()
        else:
            return {"username":username,"id":user_id}
    except JWTError:
        raise get_user_exception()


@app.post("/create/user")
async def create_user(create_user:CreateUser,db:Session=Depends(get_db)):
    create_user_model=models.Users()
    create_user_model.username=create_user.username
    create_user_model.email=create_user.email
    create_user_model.first_name=create_user.first_name
    create_user_model.last_name=create_user.last_name

    hash_password=get_password_hash(create_user.password)

    create_user_model.hashed_password=hash_password
    create_user_model.is_active=True

    db.add(create_user_model)
    db.commit()
    return {"user_added":"Sucessfully added user"}


@app.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        #raise HTTPException(status_code=404,detail="User not found")
        raise token_exceptions()
    token_expires=timedelta(minutes=20)
    token=create_access_token(user.username,user.id,expires_delta=token_expires)
    return {"token":token}



def get_user_exception():
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Autenticate":"Bearer"})
    return credentials_exception


def token_exceptions():
    token_exceptions_respons=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",
    headers={"WWW-Autenticate":"Bearer"})
    return token_exceptions_respons