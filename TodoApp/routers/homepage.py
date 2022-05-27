from http.client import responses
import sys
sys.path.append("..")

from fastapi import APIRouter,Depends,HTTPException,Request,Form
from database import engine,SessionLocal
import models
from starlette.responses import RedirectResponse
from starlette import status

from sqlalchemy.orm import Session

from pydantic import BaseModel,Field,ValidationError, validator
from typing import Optional

from .auth import get_current_user,get_user_exception,get_current_user_cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router=APIRouter(tags=["Homepage"],responses={404:{"Description":"Not found"}})

models.Base.metadata.create_all(bind=engine)
templates=Jinja2Templates(directory="templates")



@router.get("/",response_class=HTMLResponse)
async def get_page(request: Request):
    # return HTMLResponse(content="homepage.html", status_code=200)
    return templates.TemplateResponse("homepage.html",{"request":request})