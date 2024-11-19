from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./bots.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    message_id = Column(Integer, nullable=True)
    created_at = Column(String, nullable=True,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    message =  Column(String, nullable=True)

class BannedBot(Base):
    __tablename__ = "banned_bots"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    bot_created_at = Column(String, nullable=True)
    created_at = Column(String, nullable=True,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class GroupsData(Base):
    __tablename__ = "groups"
    id = Column(String,primary_key=True,)#Integer,  index=True)
    link =  Column(String)
    title =  Column(String)

Base.metadata.create_all(bind=engine)
