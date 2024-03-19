from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Application(Base):
    __tablename__ = 'application'
    number = Column(Integer, primary_key=True)
    student_number = Column(Integer)
    name = Column(String)
    surname = Column(String)
    id_number = Column(String)
    email = Column(String)
    course = Column(String)
    academic_background = Column(String)
    experience = Column(String)
    skills = Column(String)


engine = create_engine('sqlite:///jobs.db')
Base.metadata.create_all(engine)
