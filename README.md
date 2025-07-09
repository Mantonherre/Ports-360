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


## Cómo ejecutar context-adapter

Ejecuta el microservicio y el broker MQTT con Docker Compose:

```bash
docker compose up --build context-adapter mosquitto
```

El servicio quedará disponible en `http://localhost:8010`.


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

## Uso del simulador de sensores

Para generar datos de prueba puedes ejecutar el simulador:

```bash
python tools/sensor_sim/sensor_sim.py --config tools/sensor_sim/config.yaml --mqtt-host localhost --rate 1
```
