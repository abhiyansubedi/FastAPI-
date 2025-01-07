from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import Mapped
from database import Base,engine

def create_tables():
    Base.metadata.create_all(engine)


class Todo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(40), nullable=False)
    description: Mapped[str] = Column(String(255), nullable=False)
    done: Mapped[bool] = Column(Boolean)
