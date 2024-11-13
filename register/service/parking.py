import random
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from models.parking import Parking, Parkseat, Payment
from schema.parking import ParkingBase
from service.database import db_url

engine = create_engine(db_url, echo=True)

# parknum 랜덤 할당 함수
def random_parknum(db: Session) -> int:
    existing_parknums = {row[0] for row in db.query(Parkseat.parknum).all()}
    return random.choice([num for num in range(1, 101) if num not in existing_parknums])

# 차량 등록 함수
def register(db: Session, parking_data: ParkingBase):

    # parking 테이블에 저장
    parking = Parking(**parking_data.model_dump())
    db.add(parking)
    db.commit()
    db.refresh(parking)

    # parknum 생성 후 Parkseat에 저장
    parknum = random_parknum(db)
    new_parkseat = Parkseat(carnum=parking.carnum, barrier=parking.barrier, parknum=parknum)
    db.add(new_parkseat)
    db.commit()



# 입차 내역 전부 조회
def carlists(db: Session, parknum: str):
    query = (
        db.query(Parkseat.carnum, Parking.intime, Parking.pno)
        .join(Parking, Parking.carnum == Parkseat.carnum)
        .filter(Parkseat.carnum.like(f"%{parknum}"))
    )
    result = query.all()
    return [{"carnum": row[0], "intime": row[1], "pno": row[2]} for row in result]

# 출차 함수 / 출차 시 parkseat 정보 삭제
def set_outtime(db: Session, pno: int):
    parking = db.query(Parking).filter(Parking.pno == pno).first()

    if not parking:
        return {"error": "Car not found"}

    parking.outtime = datetime.now()
    db.commit()
    
    db.query(Parkseat).filter(Parkseat.carnum == parking.carnum).delete()
    db.commit()
    print(f"Car {parking.carnum} removed from parkseat due to payment completion.")
    
