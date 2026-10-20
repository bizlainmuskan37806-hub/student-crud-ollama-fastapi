from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Query, Student
from app.ollama_client import OllamaError, generate_answer
from app.schemas import AskRequest, AskResponse

api_router = APIRouter()


def _student_context(db: Session) -> str:
    students = db.query(Student).order_by(Student.id.asc()).all()

    if not students:
        return "No students in the database."

    lines = [
        f"- id={s.id}, name={s.name}, email={s.email}, age={s.age}, course={s.course}"
        for s in students
    ]
    return "\n".join(lines)


@api_router.post("/ask", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,
    db: Session = Depends(get_db),
):
    context = _student_context(db) if payload.use_student_context else None

    try:
        answer = await generate_answer(payload.question, context=context)
    except OllamaError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    saved_id = None

    if payload.save:
        record = Query(question=payload.question, answer=answer)
        db.add(record)

        try:
            db.commit()
            db.refresh(record)
            saved_id = record.id
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save the question and answer.",
            ) from exc

    return AskResponse(
        question=payload.question,
        answer=answer,
        saved_id=saved_id,
    )
