from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base

class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    star = Column(String, index=True)