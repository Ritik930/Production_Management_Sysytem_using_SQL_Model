from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from .routers import operator,manager,auth_router
from .models import *
from .database import engine

SQLModel.metadata.create_all(engine)

app = FastAPI(title = "Production Management System " )

app.include_router(auth_router.router)
app.include_router(operator.router)
app.include_router(manager.router)


