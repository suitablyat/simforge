SHELL := /bin/bash

.PHONY: dev down logs migrate seed fmt lint \
        rebuild-web rebuild-all hard-reset clean-web-cache \
        health status ps restart

dev:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

rebuild-web:
	docker compose down
	docker compose build --no-cache web
	docker compose up -d --force-recreate web

rebuild-all:
	docker compose down
	docker compose build --no-cache
	docker compose up -d --force-recreate

hard-reset:
	docker compose down -v
	docker compose build --no-cache --pull
	docker compose up -d --force-recreate

clean-web-cache:
	docker compose exec web sh -lc 'rm -rf .next node_modules/.cache .turbo || true'
	docker compose exec web sh -lc 'pnpm store prune || true'
	docker compose restart web

health:
	docker inspect --format='{{ .Name }} => {{range .State.Health.Log}}{{ .ExitCode }}: {{ .Output }}{{end}}' $$(docker ps -q)

status:
	docker compose ps

restart:
	docker compose restart

migrate:
	@echo "TODO: migrations"

seed:
	@echo "TODO: seed"

fmt:
	@echo "TODO: fmt"

lint:
	@echo "TODO: lint"
