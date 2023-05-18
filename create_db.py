from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from configuration import DATABASE_URL

Base = declarative_base()


class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow)
    questions = relationship('Questions', backref='quiz')

    def json(self):
        return {
            'id_quiz': self.id,
            'questions': [q.json() for q in self.questions],
        }


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    id_question = Column(Integer, unique=True, index=True)
    question = Column(String, unique=True)
    answer = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    quiz_id = Column(Integer, ForeignKey('quiz.id'))

    def json(self):
        return {
            'id_question': self.id_question,
            'question': self.question,
            'answer': self.answer,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        }


def connect_db():
    """Function to connect to database and return session object.
    :return: Session object
    """

    try:
        engine = create_engine(DATABASE_URL, connect_args={})
        session = Session(bind=engine.connect())
        yield session
    finally:
        session.close()


def start_db():
    """Function to start the database
    :return: None
    """

    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    Base.metadata.create_all(bind=engine)
    session.close()
