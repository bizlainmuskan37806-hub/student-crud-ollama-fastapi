from typing import List

from fastapi import Depends, HTTPException, status,Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.routes.base import api_router
from app.schemas import StudentRead


def get_student_or_404(db: Session, student_id: int) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()  #finds a student by ID
    if student is None:#handles a missing student 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@api_router.get("/students", response_model=List[StudentRead])
def list_students(# validates pagination
    skip: int = Query(default=0, ge=0),#must be zero or greater
    limit: int = Query(default=50, ge=1, le=200),#must be between 1 and 200
    db: Session = Depends(get_db),
):
    return (
        db.query(Student)
        .order_by(Student.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@api_router.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(db, student_id)
