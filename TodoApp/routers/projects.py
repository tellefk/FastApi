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


router=APIRouter(prefix="/projects",tags=["Prosjekt"],responses={404:{"Description":"Not found"}})

models.Base.metadata.create_all(bind=engine)
templates=Jinja2Templates(directory="templates")

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/",response_class=HTMLResponse)
async def read_all_by_user(request:Request,db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    
    projects=db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
    return templates.TemplateResponse("home.html",{"request":request,"projects":projects,"user":user})


@router.get("/add-project",response_class=HTMLResponse)
async def add_project(request:Request):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("add-project.html",{"request":request})
    

@router.post("/add-project",response_class=HTMLResponse)
async def add_projects(request:Request,title:str=Form(...),description:str=Form(...),priority:int=Form(...),db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    todo_model=models.Todos()
    todo_model.priority=priority
    todo_model.complete=False
    todo_model.title=title
    todo_model.description=description
    todo_model.owner_id=user.get("id")
    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/projects",status_code=status.HTTP_302_FOUND)

@router.get("/edit-project/{project_id}",response_class=HTMLResponse)
async def edit_project(request:Request,project_id:int,db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    project=db.query(models.Todos).filter(models.Todos.id==project_id).first()
    return templates.TemplateResponse("edit-project.html",{"request":request,"prosjektTest":project,"user":user})

@router.post("/edit-project/{project_id}",response_class=HTMLResponse)
async def add_projects(request:Request,project_id:str,title:str=Form(...),description:str=Form(...),priority:int=Form(...),db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    project=db.query(models.Todos).filter(models.Todos.id==project_id).first()
    project.priority=priority
    project.title=title
    project.description=description
    db.add(project)
    db.commit()
    return RedirectResponse(url="/projects",status_code=status.HTTP_302_FOUND)


@router.get("/delete/{project_id}",response_class=HTMLResponse)
async def delete_projects(request:Request,project_id:str,db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    project_data=db.query(models.Todos).filter(models.Todos.id==project_id).filter(models.Todos.owner_id==user.get("id")).first()
    if project_data is None:
         return RedirectResponse(url="/projects",status_code=status.HTTP_302_FOUND)
    db.query(models.Todos).filter(models.Todos.id==project_id).delete()
    db.commit()
    return RedirectResponse(url="/projects",status_code=status.HTTP_302_FOUND)


@router.get("/{project_id}",response_class=HTMLResponse)
async def get_project(request:Request,project_id:int,db:Session=Depends(get_db)):
    user=await get_current_user_cookie(request)
    if user is None:
        return RedirectResponse(url="/auth",status_code=status.HTTP_302_FOUND)
    project_data=db.query(models.Todos).filter(models.Todos.id==project_id).filter(models.Todos.owner_id==user.get("id")).first()
    if project_data is None:
        return RedirectResponse(url="/projects",status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("projects.html",{"request":request,"prosjektTest":project_data,"user":user})
