up:
	docker compose up -d

down:
	docker compose down -v

lint:
	ruff check .
	mypy .

test:
	pytest -q

migrate:
	alembic upgrade head

seed:
	python -m app.db.seed

eval:
	python eval/run_eval.py
