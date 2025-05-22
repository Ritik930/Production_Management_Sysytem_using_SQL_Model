from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

# Base Models
class RollingParametersBase(SQLModel):
    part_name: str = Field(index=True, unique=True)
    machine_name: str

# Table Models
class RollingParameters(RollingParametersBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_: date = Field(default=date.today(), nullable=False)
    time_stamp: datetime = Field(default_factory=datetime.now, nullable=False)
    shift: str = Field(default="Day")
    coolant_temperature: Optional[float] = Field(default=None)
    machining_angle: Optional[float] = Field(default=None)
    chuck_speed: Optional[float] = Field(default=None)
    is_completed: bool = Field(default=False)

# Create/Update Schemas
class RollingParametersCreate(RollingParametersBase):
    pass

class RollingParametersUpdate(SQLModel):
    coolant_temperature: Optional[float] = None
    machining_angle: Optional[float] = None
    chuck_speed: Optional[float] = None
    is_completed: Optional[bool] = None

# Response Models
class RollingParametersResponse(RollingParametersBase):
    id: int
    date_: date
    time_stamp: datetime
    shift: str
    coolant_temperature: Optional[float] = None
    machining_angle: Optional[float] = None
    chuck_speed: Optional[float] = None
    is_completed: bool

    class Config:
        from_attributes = True

# Additional Models
class ProductionStats(SQLModel):
    total_parts: int
    machine_wise: dict[str, int]

class ShiftInfo(SQLModel):
    shift: str
    current_time: str

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    is_active: Optional[bool] = Field(default=False)
    is_superuser: bool = Field(default=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserRead(UserBase):
    id: int

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None