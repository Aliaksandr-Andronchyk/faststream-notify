import pytest
from faststream.rabbit import TestRabbitBroker
from pydantic import ValidationError

from app.main import broker, handle_lesson_booked, handle_lesson_cancelled, send_email

BOOKED_EVENT = {
    "lesson_id": 42,
    "tutor_name": "Anna",
    "student_name": "Ivan",
    "student_email": "ivan@example.com",
    "starts_at": "2026-08-01T10:00:00",
    "ends_at": "2026-08-01T11:00:00",
}


async def test_booked_event_produces_email():
    async with TestRabbitBroker(broker) as br:
        await br.publish(BOOKED_EVENT, "lesson.booked")

        handle_lesson_booked.mock.assert_called_once()
        send_email.mock.assert_called_once()
        sent = send_email.mock.call_args.args[0]
        assert sent["to"] == "ivan@example.com"
        assert sent["kind"] == "booking_confirmation"


async def test_cancelled_event_produces_email():
    async with TestRabbitBroker(broker) as br:
        await br.publish(
            {
                "lesson_id": 42,
                "tutor_name": "Anna",
                "student_name": "Ivan",
                "student_email": "ivan@example.com",
                "starts_at": "2026-08-01T10:00:00",
                "reason": "tutor is ill",
            },
            "lesson.cancelled",
        )

        handle_lesson_cancelled.mock.assert_called_once()
        sent = send_email.mock.call_args.args[0]
        assert sent["kind"] == "cancellation_notice"
        assert "tutor is ill" in sent["body"]


async def test_invalid_event_rejected():
    async with TestRabbitBroker(broker) as br:
        with pytest.raises(ValidationError):
            await br.publish({"lesson_id": "not-a-number"}, "lesson.booked")

        send_email.mock.assert_not_called()
