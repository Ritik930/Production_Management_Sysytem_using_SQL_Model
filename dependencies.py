from .database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db_session():
    return Depends(get_db)