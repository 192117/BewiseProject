import requests
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from configuration import settings
from create_db import Questions, Quiz


def save_request_number(request_number: int, session: Session) -> Quiz:
    """Save Request_number in database.
    :param request_number: Number of questions in the quiz.
    :param session: Session for working with the database
    :return: Request_number object
    """

    quiz = Quiz(number=request_number)
    session.add(quiz)
    session.commit()
    session.refresh(quiz)
    return quiz


def get_questions(request_number: int, session: Session):
    """Receives with QUESTIONS_URL <request_number> questions from the quiz and stores in the database.
    If there is a question in the database, calls itself recursively with the number of unsaved questions.
    :param request_number: Number of questions in the quiz.
    :param session: Session for working with the database
    :return: If success True
    """

    try:
        url = settings.QUESTIONS_URL
        questions_response = requests.get(url + str(request_number))
        questions_response.raise_for_status()
        questions_from_url = questions_response.json()
        quiz = save_request_number(request_number, session)
        questions = []
        for question in questions_from_url:
            questions.append(
                {
                    'id_question': question['id'],
                    'question': question['question'],
                    'answer': question['answer'],
                    'date_created': question['created_at'],
                    'quiz_id': quiz.id,
                },
            )
        result = session.bulk_save_objects([Questions(**quest) for quest in questions])
        session.commit()
        return quiz.id
    except IntegrityError:
        count = request_number - result.rowcount
        if count != 0:
            get_questions(count, session)
