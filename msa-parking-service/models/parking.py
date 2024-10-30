
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Parking(Base):
    __tablename__ = 'parking'

    pno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    carnum = Column(String(10), nullable=False)
    barrier = Column(String(5), nullable=False, default='0')
    intime = Column(DateTime, default=datetime.now)
    outtime = Column(DateTime, nullable=True)


class Parkseat(Base):
    __tablename__ = 'parkseat'

    carnum = Column(String(10), primary_key=True, nullable=False)
    barrier = Column(String(5), nullable=False, default='0')
    parknum = Column(Integer, nullable=False)

# 수정 필요
class Payment(Base):
    __tablename__ = 'payment'

    payid = Column(Integer, primary_key=True, autoincrement=True)
    payment = Column(String(50))
    paydate = Column(DateTime, nullable=True)
    parkingtime = Column(String(20), nullable=True)
    carnum = Column(String(10), ForeignKey('parking.carnum'))

# class VisitorStats(Base):
#     __tablename__ = 'visitor_stats'
#
#     sno = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     carnum = Column(String(10), nullable=False)
#     month = Column(String(10), nullable=False)
#     visitor_count = Column(Integer, nullable=False)
#
#
# class PaymentStats(Base):
#     __tablename__ = 'payment_stats'
#
#     sno = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     month = Column(String(10), nullable=False)
#     total_fee = Column(Float, nullable=False)