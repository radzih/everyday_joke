py := poetry run
python := $(py) python

.ONESHELL:

define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	poetry run black src tests
	poetry run isort src tests

.PHONY: dev-bot
dev-bot:
	$(call setup_env, .env.dev)
	PYTHONPATH=./src $(python) -m everyday_joke.bot

.PHONY: dev-docker
dev-docker:
	docker compose -f=docker-compose-dev.yml --env-file=.env.dev up

.PHONY: dev-make-migrations
dev-make-migrations:
	$(call setup_env, .env.dev)
	PYTHONPATH=./src $(py) alembic revision --autogenerate

.PHONY: dev-migrate
dev-migrate:
	$(call setup_env, .env.dev)
	PYTHONPATH=./src $(py) alembic upgrade head

.PHONY: dev-env
dev-env:
	$(call setup_env, .env.dev)
	$(filter-out $@,$(MAKECMDGOALS))

.PHONY: dev-scheduler
def-scheduler:
	$(call setup_env, .env.dev)
	PYTHONPATH=./src $(python) -m everyday_joke.scheduler

.PHONY: prod-migrate
prod-migrate:
	$(call setup_env, .env)
	PYTHONPATH=./src python -m alembic upgrade head

.PHONY: prod-bot
prod-bot:
	$(call setup_env, .env)
	python -m everyday_joke.bot

.PHONY: prod-scheduler
prod-scheduler:
	$(call setup_env, .env)
	python -m everyday_joke.scheduler

.PHONY: test-bot
test-bot:
	$(call setup_env, .env.test)
	PYTHONPATH=./src python -m everyday_joke.bot

.PHONY: test-docker
test-docker:
	docker compose -f=docker-compose-test.yml --env-file=.env.test up -d

.PHONY: tests
tests:
	$(call setup_env, .env.test)
	PYTHONPATH=./src $(python) -m pytest --disable-warnings 