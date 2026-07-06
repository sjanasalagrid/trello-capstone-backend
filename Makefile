up:
	docker compose up --build

down:
	docker compose down

restart:
	docker compose down
	docker compose up --build

logs:
	docker compose logs -f

test:
	pytest -v

lint:
	ruff check .
	black .

migrate:
	alembic upgrade head

shell:
	docker exec -it trello-backend /bin/sh