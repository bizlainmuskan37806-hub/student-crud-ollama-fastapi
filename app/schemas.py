from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    age: int = Field(..., ge=1, le=120)
    course: Optional[str] = Field(default=None, max_length=120)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=1, le=120)
    course: Optional[str] = Field(default=None, max_length=120)

    @model_validator(mode="before")
    @classmethod
    def reject_null_required_fields(cls, data):
        if isinstance(data, dict):
            for field in ("name", "email", "age"):
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")
        return data
    
class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    save: bool = True
    use_student_context: bool = True


class AskResponse(BaseModel):
    question: str
    answer: str
    saved_id: Optional[int] = None
