from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LessonBooked(BaseModel):
    lesson_id: int
    tutor_name: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    student_email: EmailStr
    starts_at: datetime
    ends_at: datetime


class LessonCancelled(BaseModel):
    lesson_id: int
    tutor_name: str = Field(min_length=1)
    student_name: str = Field(min_length=1)
    student_email: EmailStr
    starts_at: datetime
    reason: str | None = None


class EmailNotification(BaseModel):
    to: EmailStr
    subject: str
    body: str
    kind: Literal["booking_confirmation", "cancellation_notice"]
