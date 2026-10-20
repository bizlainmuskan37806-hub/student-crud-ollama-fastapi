from fastapi import Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.base import api_router
from app.routes.get_student import get_student_or_404


@api_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(db, student_id)
    db.delete(student)
    db.commit()
