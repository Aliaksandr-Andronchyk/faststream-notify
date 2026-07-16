# faststream-notify

![CI](https://github.com/SashaAndronchyk/faststream-notify/actions/workflows/ci.yml/badge.svg)

Event-driven notification microservice for a lesson-booking platform (companion to
[lesson-booking-api](https://github.com/SashaAndronchyk/lesson-booking-api)).

**Stack:** FastStream · RabbitMQ · pydantic v2 · pytest · Docker Compose · GitHub Actions

## What it does

Consumes domain events and turns them into email notifications:

```
lesson.booked    ──▶ handle_lesson_booked    ──▶ notifications.email ──▶ send_email
lesson.cancelled ──▶ handle_lesson_cancelled ──▶ notifications.email ──▶ send_email
```

- Events are validated with **pydantic v2** schemas — malformed payloads are rejected
- Message formatting is pure, broker-free code (`app/notifications.py`) — unit-tested directly
- Handlers are integration-tested with FastStream's **in-memory `TestRabbitBroker`** —
  no RabbitMQ needed to run the suite
- `send_email` is a demo transport (logs the message); swap in SMTP/SES in production

## Run

```bash
docker compose up --build      # RabbitMQ (with management UI on :15672) + worker
```

Publish a test event from another shell:

```bash
python -c "
import asyncio
from faststream.rabbit import RabbitBroker

async def main():
    async with RabbitBroker('amqp://guest:guest@localhost:5672/') as broker:
        await broker.publish({
            'lesson_id': 1, 'tutor_name': 'Anna', 'student_name': 'Ivan',
            'student_email': 'ivan@example.com',
            'starts_at': '2026-08-01T10:00:00', 'ends_at': '2026-08-01T11:00:00',
        }, 'lesson.booked')

asyncio.run(main())
"
```

The worker logs the confirmation email it would send.

## Tests

```bash
pip install -e ".[dev]"
pytest -v        # runs fully in-memory, no broker required
```
