from datetime import datetime, timedelta, time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Schema
from sqlmodel import Session, select
from .. import models, models
from ..database import get_session
from ..models import ShiftInfo, RollingParametersCreate
from ..utils import determine_shift

router = APIRouter(
    prefix="/operator",
    tags=["operator"]
)

# Get Current shift

@router.get("/Current_Shift", response_model=ShiftInfo)
def determine_shift():
    now = datetime.now().time()
    shift_a_start = time(7, 0)
    shift_b_start = time(19, 0)

    shift = "A" if shift_a_start <= now < shift_b_start else "B"
    return {
        "shift": shift,
        "current_time": now.strftime("%H:%M:%S")
    }

#Scan Part Name

@router.post("/scan_Part_Name/", response_model=models.RollingParametersResponse)
def scan_part(
        part_data: models.RollingParametersCreate,
        db: Session = Depends(get_session)
):
    existing_part = db.exec(select(models.RollingParameters).where(
        models.RollingParameters.part_name == part_data.part_name
    )).first()

    if existing_part:
        raise HTTPException(status_code=400, detail="Part already scanned")

    shift_data = determine_shift()
    db_part = models.RollingParameters(
        part_name=part_data.part_name,
        machine_name=part_data.machine_name,
        shift=shift_data["shift"],
        is_completed=False
    )

    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

#Update temp,angle,speed

@router.post("/update/{part_name}", response_model=models.RollingParametersResponse)
async def update_parameters(
        part_name: str,
        params: models.RollingParametersUpdate,db: Session = Depends(get_session)):
    db_part = db.exec(select(models.RollingParameters).where(
        models.RollingParameters.part_name == part_name
    )).first()

    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    update_data = params.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_part, field, value)

    if update_data:
        db_part.is_completed = True


    db_part.is_completed = True
    db.commit()
    db.refresh(db_part)
    return db_part

# delete Part_Name

@router.delete("/delete/{part_name}")
def delete_part(part_name: str, db: Session = Depends(get_session)):
    db_part = db.exec(select(models.RollingParameters).where(
        models.RollingParameters.part_name == part_name
    )).first()

    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")

    db.delete(db_part)
    db.commit()
    return {"message": "Part deleted successfully"}