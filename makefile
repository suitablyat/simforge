SHELL := /bin/bash

.PHONY: dev down logs migrate seed fmt lint

dev:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

migrate:
	# Platzhalter: hier DB-Migrations-Command einhängen, z. B. alembic upgrade head
	@echo "TODO: migrations"

seed:
	# Platzhalter: Seed-Script, falls vorhanden
	@echo "TODO: seed"

fmt:
	# Optional: Linter/Formatter für api/web/worker
	@echo "TODO: fmt"

lint:
	@echo "TODO: lint"
