from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlmodel import func
from datetime import date
from .. import models, models
from ..database import get_session
from ..auth import get_current_active_user

router = APIRouter(
    prefix="/manager",
    tags=["manager"]
)

#Daily Production

@router.get("/daily-production/", response_model=models.ProductionStats)
def get_daily_production(date_: date = date.today(),db: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_active_user)):
    total_parts = db.exec(select(func.count(models.RollingParameters.id)).where(models.RollingParameters.date_ == date_)).one()

    machine_counts = db.exec(select(models.RollingParameters.machine_name,func.count(models.RollingParameters.id)
    ).where(models.RollingParameters.date_ == date_).group_by(models.RollingParameters.machine_name)).all()

    return {
        "total_parts": total_parts,
        "machine_wise": dict(machine_counts)
    }

#Weekly Production

@router.get("/weekly_production/", response_model=models.ProductionStats)
def get_weekly_production(
        year: int,
        month: int,
        week: int,
        db: Session = Depends(get_session),
        current_user: models.User = Depends(get_current_active_user)
):

    start_date = date.fromisocalendar(year, week, 1)

    end_date = date.fromisocalendar(year, week, 7)

    total_parts = (db.exec(select(func.count(models.RollingParameters.id)).where(models.RollingParameters.date_ >= start_date,models.RollingParameters.date_ <= end_date
        )).one()
    )

    machine_counts = (
        db.exec(select(models.RollingParameters.machine_name, func.count(models.RollingParameters.id))
        .where(models.RollingParameters.date_ >= start_date,models.RollingParameters.date_ <= end_date)
        .group_by(models.RollingParameters.machine_name)).all()
    )

  #  machine_wise_counts = {
   ### }
    return {
        "total_parts": total_parts,
        "machine_wise":dict(machine_counts)
    }

#monthly Production

@router.get("/monthly-production/", response_model=models.ProductionStats)
def get_monthly_production(
        year: int,
        month: int,
        db: Session = Depends(get_session),
        current_user: models.User = Depends(get_current_active_user)
):
    total_parts = db.exec(select(func.count(models.RollingParameters.id)).where(
        func.extract('year', models.RollingParameters.date_) == year,
        func.extract('month', models.RollingParameters.date_) == month
    )).one()

    machine_counts = db.exec(select(
        models.RollingParameters.machine_name,
        func.count(models.RollingParameters.id)
    ).where(
        func.extract('year', models.RollingParameters.date_) == year,
        func.extract('month', models.RollingParameters.date_) == month
    ).group_by(
        models.RollingParameters.machine_name
    )).all()

    return {
        "total_parts": total_parts,
        "machine_wise": dict(machine_counts)
    }

#Get Data Machine Wise

@router.get("/Machine_Wise/{machine_name}")
def get_machineWise_Production(machine_name: str, db: Session = Depends(get_session),
        current_user: models.User = Depends(get_current_active_user)):
    total_parts = db.exec(
        select(func.count(models.RollingParameters.id))
        .where(models.RollingParameters.machine_name == machine_name)
    ).one()

    return{
        "total_parts" : total_parts
    }

#Get all DATA

@router.get("/all")
async def get_all_production_data(skip: int = 0,limit: int = 100,db: Session = Depends(get_session), current_user: models.User = Depends(get_current_active_user)):

    total_count = db.exec(select(func.count(models.RollingParameters.id))).one()

    data = db.exec(select(models.RollingParameters)
        .order_by(models.RollingParameters.time_stamp.desc())
        .offset(skip)
        .limit(limit)
                   ).all()

    return {
        "data": data,
        "count": total_count
    }