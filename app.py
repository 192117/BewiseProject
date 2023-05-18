import fastapi.openapi.utils as fu
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from requests.exceptions import HTTPError
from sqlalchemy.orm import Session, joinedload

from create_db import Quiz, connect_db, start_db
from models import QuestionsNumber, QuizResponse
from utils import get_questions

app = FastAPI(title='BewiseProject API', description='A web service that provides an API for '
                                                     'getting random quiz questions from public jService API')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation exception."""
    return JSONResponse(
        status_code=400,
        content={'error': 'Данные не прошли валидацию!'},
    )


fu.validation_error_response_definition = {
    'title': 'HTTPValidationError',
    'type': 'object',
    'properties': {
        'error': {'title': 'Message', 'type': 'string'},
    },
}


@app.on_event('startup')
async def startup_event():
    start_db()


@app.on_event('shutdown')
async def shutdown_event():
    connect_db().close()


@app.post('/quiz/', response_model=QuizResponse)
async def add_object(qn: QuestionsNumber, db: Session = Depends(connect_db)):
    try:
        data = qn.dict()
        if get_questions(data['questions_num'], db):
            request_questions = db.query(Quiz).options(joinedload(Quiz.questions))\
                .order_by(Quiz.date_created.desc()).limit(2).all()
            if len(request_questions) > 1:
                return JSONResponse({'questions': request_questions[-1].json()}, status_code=200)
            else:
                return JSONResponse({'questions': []}, status_code=200)
    except HTTPError as exception:
        raise HTTPException(status_code=500, detail=str(exception))
