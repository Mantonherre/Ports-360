# Smart Port Alicante

Monorepo for the Smart Port Alicante MVP. It provides a basic layout for Python
microservices and a React front-end with Docker based development and CI.

## Quickstart

```bash
git clone <repo-url>
cd smartport
# or if already inside
docker compose up --build
```

The sample FastAPI service is available at [http://localhost:8000/docs](http://localhost:8000/docs).


## API documentation

The OpenAPI specification lives under `docs/api/openapi.yaml`. To generate an
HTML version using [Redoc](https://github.com/Redocly/redoc), run:

```bash
npx redoc-cli bundle docs/api/openapi.yaml -o docs/api/index.html
```

## Running tests

Install development dependencies and execute `pytest`:

```bash
pip install -r requirements-dev.txt
pytest
```
