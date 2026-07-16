from datetime import datetime

from app.notifications import booking_confirmation, cancellation_notice
from app.schemas import LessonBooked, LessonCancelled

BOOKED = LessonBooked(
    lesson_id=1,
    tutor_name="Anna",
    student_name="Ivan",
    student_email="ivan@example.com",
    starts_at=datetime(2026, 8, 1, 10, 0),
    ends_at=datetime(2026, 8, 1, 11, 0),
)


def test_booking_confirmation_format():
    note = booking_confirmation(BOOKED)
    assert note.to == "ivan@example.com"
    assert note.kind == "booking_confirmation"
    assert "01.08.2026 10:00" in note.subject
    assert "Anna" in note.body
    assert "10:00–11:00" in note.body


def test_cancellation_notice_with_reason():
    event = LessonCancelled(
        lesson_id=1,
        tutor_name="Anna",
        student_name="Ivan",
        student_email="ivan@example.com",
        starts_at=datetime(2026, 8, 1, 10, 0),
        reason="tutor is ill",
    )
    note = cancellation_notice(event)
    assert note.kind == "cancellation_notice"
    assert "tutor is ill" in note.body


def test_cancellation_notice_without_reason():
    event = LessonCancelled(
        lesson_id=1,
        tutor_name="Anna",
        student_name="Ivan",
        student_email="ivan@example.com",
        starts_at=datetime(2026, 8, 1, 10, 0),
    )
    note = cancellation_notice(event)
    assert "Reason:" not in note.body
