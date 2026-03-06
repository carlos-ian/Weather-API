from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    history = relationship("SearchHistory", back_populates="user")

class SearchHistory(Base):
    __tablename__ = "searchHistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city_name = Column(String, nullable=False)
    temp_current = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    feels_like = Column(Float)
    rain_prob = Column(Float)
    condition_desc = Column(String)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="history")