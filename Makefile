.PHONY: up down logs ps fmt lint

up:
	docker-compose up --build -d

down:
	docker-compose down -v

logs:
	docker-compose logs -f --tail=200

ps:
	docker-compose ps

fmt:
	python -m black services migrator

lint:
	python -m flake8 services migrator
