# Everyday joke bot 
This is a telegram bot where you can subscribe for receiving jokes every day. 

# Dependencies
## Infrastucture
- [Postgres](https://www.postgresql.org/docs/current/index.html) — Database
- [RabbitMQ](https://www.rabbitmq.com/documentation.html) — Message broker
- [Docker](https://docs.docker.com/) — Containerization platform
## Key Python libraries
- [aiogram](https://docs.aiogram.dev/en/latest/) — Async framework for telegram bots
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) — ORM
- [Poetry](https://python-poetry.org/docs/) — Dependency management
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — Database migrations
- [aio-pika](https://aio-pika.readthedocs.io/en/latest/)— Client for RabbitMQ



# How to run
1. Clone the repository
2. Create `.env` file in the root of the project and fill it with the following variables:
```
TG_BOT_TOKEN=<your telegram bot token>

DB_USER=<your db user>
DB_PASSWORD=<your db password>
DB_NAME=<your db name>
DB_PORT=<your db port>
DB_HOST=<your db host>

RABBITMQ_PORT=<your rabbitmq port>
RABBITMQ_HOST=<your rabbitmq host>
RABBITMQ_USER=<your rabbitmq user>
RABBITMQ_PASS=<your rabbitmq password>

SCHEDULER_TIME=<your scheduler time examples: 15:00, 13:30, 09:00>
SCHEDULER_TIMEZONE=<timezone example: Europe/Kiev>
```
3. Run `docker-compose up -d` to start the containers

# Todo
- [ ] Add tests
- [X] Export business logic to separate module