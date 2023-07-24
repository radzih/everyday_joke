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
	poetry run black --line-length=79 src
	poetry run isort src

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


