import logging

from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

from app.config import settings
from app.notifications import booking_confirmation, cancellation_notice
from app.schemas import EmailNotification, LessonBooked, LessonCancelled

logging.basicConfig(level=logging.INFO)

broker = RabbitBroker(settings.rabbit_url)
app = FastStream(broker)


@broker.subscriber("lesson.booked")
@broker.publisher("notifications.email")
async def handle_lesson_booked(event: LessonBooked, logger: Logger) -> EmailNotification:
    logger.info("Booking confirmation for lesson %s -> %s", event.lesson_id, event.student_email)
    return booking_confirmation(event)


@broker.subscriber("lesson.cancelled")
@broker.publisher("notifications.email")
async def handle_lesson_cancelled(event: LessonCancelled, logger: Logger) -> EmailNotification:
    logger.info("Cancellation notice for lesson %s -> %s", event.lesson_id, event.student_email)
    return cancellation_notice(event)


@broker.subscriber("notifications.email")
async def send_email(notification: EmailNotification, logger: Logger) -> None:
    # Demo transport: a real deployment would hand this to an email provider (SMTP/SES/…).
    logger.info(
        "[EMAIL:%s] to=%s subject=%r", notification.kind, notification.to, notification.subject
    )
