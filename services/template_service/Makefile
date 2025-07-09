.PHONY: run lint test docker-build

run:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

lint:
black .
ruff .

test:
pytest -q

docker-build:
docker build -t template_service:local .
