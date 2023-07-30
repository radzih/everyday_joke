# Everyday joke bot 
This is a simple telegram bot where you can subscribe for receiving jokes every day. 
Also you can unsubscribe from receiving jokes.

# Tech Stack
- Python 3.10
- Docker
- PostgreSQL
- SQLAlchemy
- aiogram
- RabbitMQ
- Poetry
- Makefile

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
```