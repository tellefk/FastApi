from fastapi import FastAPI
from database import engine
import models
from routers import auth,todos,spuntTest,projects
from starlette.staticfiles import StaticFiles
models.Base.metadata.create_all(bind=engine)


app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(spuntTest.router)
app.include_router(projects.router)