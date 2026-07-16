"""Pure formatting logic — kept free of broker concerns so it is trivially unit-testable."""

from app.schemas import EmailNotification, LessonBooked, LessonCancelled

TIME_FORMAT = "%d.%m.%Y %H:%M"


def booking_confirmation(event: LessonBooked) -> EmailNotification:
    starts = event.starts_at.strftime(TIME_FORMAT)
    ends = event.ends_at.strftime("%H:%M")
    return EmailNotification(
        to=event.student_email,
        subject=f"Lesson confirmed: {starts}",
        body=(
            f"Hi {event.student_name}!\n\n"
            f"Your lesson with {event.tutor_name} is confirmed "
            f"for {starts}–{ends}.\n\n"
            f"See you online!"
        ),
        kind="booking_confirmation",
    )


def cancellation_notice(event: LessonCancelled) -> EmailNotification:
    starts = event.starts_at.strftime(TIME_FORMAT)
    reason = f"\nReason: {event.reason}" if event.reason else ""
    return EmailNotification(
        to=event.student_email,
        subject=f"Lesson cancelled: {starts}",
        body=(
            f"Hi {event.student_name},\n\n"
            f"Unfortunately your lesson with {event.tutor_name} "
            f"scheduled for {starts} was cancelled.{reason}\n\n"
            f"Please pick another slot."
        ),
        kind="cancellation_notice",
    )
