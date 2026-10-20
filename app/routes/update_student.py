from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.base import api_router
from app.routes.get_student import get_student_or_404
from app.schemas import StudentCreate, StudentRead, StudentUpdate


@api_router.put("/students/{student_id}", response_model=StudentRead)
def replace_student(student_id: int, payload: StudentCreate, db: Session = Depends(get_db)):
    student = get_student_or_404(db, student_id)
    student.name = payload.name
    student.email = payload.email
    student.age = payload.age
    student.course = payload.course
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists",
        ) from exc
    db.refresh(student)
    return student


@api_router.patch("/students/{student_id}", response_model=StudentRead)
def patch_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = get_student_or_404(db, student_id)
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    for field, value in updates.items():
        setattr(student, field, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists",
        ) from exc
    db.refresh(student)
    return student
