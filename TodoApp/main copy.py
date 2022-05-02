from re import A
from fastapi import FastAPI,Depends,HTTPException
from database import engine,SessionLocal
import models
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from typing import Optional
from routers.auth import get_current_user,get_user_exception
from routers import auth


app=FastAPI()

app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title:str
    description:Optional[str]
    priority:int=Field(gs=0,ls=6,description="priority most be between 1 or 5")
    complete:bool
   



@app.get("/")
async def read_all(db:Session=Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/todo/user")
async def read_all_by_user(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()



"""
Uten user info: User med owner ID ligger i jwt token
"""
# @app.get("/todo/{todo_id}")
# async def read_todo(todo_id:int,db:Session=Depends(get_db)):
#     todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     else:
#         raise HTTPException(status_code=404,detail="Could not find todo")


# @app.post("/")
# async def create_todo(todo:Todo,db:Session=Depends(get_db)):
#     todo_model = models.Todos()
#     todo_model.title=todo.title
#     todo_model.description=todo.description
#     todo_model.priority=todo.priority
#     todo_model.complete=todo.complete
#     db.add(todo_model)
#     db.commit()
#     return {"status_code":201,"Transaction":"Success"}


# @app.put("/{todo_id}")
# async def update_todos(todo_id:int,todo:Todo,db:Session=Depends(get_db)):
#     todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail="Could not find todo")
#     else:
#         todo_model.title=todo.title
#         todo_model.description=todo.description
#         todo_model.priority=todo.priority
#         todo_model.complete=todo.complete
#         db.add(todo_model)
#         db.commit()
#         return {"status_code":201,"Transaction":"Success"}

@app.get("/todo/{todo_id}")
async def read_todo(todo_id:int,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.id==user.get("id")).first()
    if todo_model is not None:
        return todo_model
    else:
        raise get_user_exception()


@app.post("/")
async def create_todo(todo:Todo,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete
    todo_model.owner_id=user.get("id")
    db.add(todo_model)
    db.commit()
    return {"status_code":201,"Transaction":"Success"}


@app.put("/{todo_id}")
async def update_todos(todo_id:int,todo:Todo,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if user is None:
        raise get_user_exception()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Could not find todo")
    else:
        todo_model.title=todo.title
        todo_model.description=todo.description
        todo_model.priority=todo.priority
        todo_model.complete=todo.complete
        db.add(todo_model)
        db.commit()
        return {"status_code":201,"Transaction":"Success"}

@app.delete("/{todo_id}")
async def delete_todos(todo_id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if user is None:
        raise get_user_exception()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Could not find todo")
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).delete()
    db.commit()
    return {"status_code":201,"Transaction":"Success"}


def successfulResponse():
    return {"status_code":201,"Transaction":"Success"}

def HTTPExceptionRespons():
    HTTPException(status_code=404,detail="Could not find todo")
    