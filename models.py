from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class QuestionsNumber(BaseModel):
    """Model for describing the body of the request for the url /quiz/ ."""
    questions_num: int

    @validator('questions_num')
    def validate_questions_num(cls, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError


class QuestionResponse(BaseModel):
    """Model for describing the description of the response of the objects of the Question table."""

    id_question: int
    question: str
    answer: str
    date_created: datetime


class QuizResponse(BaseModel):
    """Model for describing the description of the response of the objects of the Quiz table."""

    id_quiz: int
    questions: List[QuestionResponse]
