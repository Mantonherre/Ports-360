# Smart Port Alicante

Monorepo for the Smart Port Alicante MVP. It provides a basic layout for Python
microservices and a React front-end with Docker based development and CI.

## Quickstart

```bash
git clone <repo-url>
cd Ports-360
# or if already inside
cp infra/.env.example infra/.env
docker compose up --build
```

`infra/.env` contains the credentials used by the containers. Copying the
example file is required before starting the stack, otherwise many services will
fail to boot.

The sample FastAPI service is available at [http://localhost:8000/docs](http://localhost:8000/docs).

Add `ports360.online` to `/etc/hosts` pointing to `127.0.0.1` to access the stack through Traefik using HTTPS.

Traefik exposes the internal services under distinct path prefixes:

- `/api/*` forwards to the Context Adapter
- `/db/*` forwards to the Timeseries Writer
- `/gql/*` forwards to the Twin Core
- `/ws` forwards to the Context Adapter WebSocket endpoint and is
  available over `ws://` and `wss://`

These prefixes are stripped, so the backends keep their original routes such as `/health` or `/metrics`.

All passwords are defined in `infra/.env`. Duplicate `infra/.env.example` and adjust values before running the stack.


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

El simulador requiere que haya un broker MQTT en ejecución. Si no está disponible
recibirás errores de "Connection refused".

## Otros servicios

Cada microservicio incluye instrucciones en su propio directorio, aunque a
continuación se resumen los comandos más habituales:

### Context Adapter

```bash
cd services/context_adapter
docker build -t context-adapter .
docker run -e MQTT_HOST=mqtt -p 8010:8010 context-adapter
```

### Twin Core

```bash
cd services/twin_core
npm install
npm run build
npm start
```

### Timeseries Writer

```bash
cd services/timeseries
docker build -t timeseries-writer .
docker run -e PGHOST=postgres -e MQTT_HOST=mqtt -p 8020:8020 timeseries-writer
```

### Ejemplo de consulta GraphQL

El servicio Twin Core protege su API frente a ataques CSRF, por lo que las
peticiones deben incluir las cabeceras adecuadas. Si accedes al servicio a
través de Traefik, la ruta es `http://localhost:8000/gql`; de manera directa, es
`http://localhost:8030/`.

Ejemplo con `curl`:

```bash
curl -X POST http://localhost:8000/gql \
  -H 'Content-Type: application/json' \
  -H 'x-apollo-operation-name: Test' \
  -d '{"query":"{ __typename }"}'
```

### Dashboard web

```bash
cd ui/dashboard
npm install
npm run dev
```

## Documentación adicional

El directorio `docs/` contiene información detallada sobre la arquitectura y la operación del proyecto:

- `docs/architecture/` incluye diagramas *Mermaid* de cada servicio.
- `docs/observability.md` explica la exposición de métricas en Prometheus y Grafana.
- `docs/security.md` describe el flujo de autenticación con Keycloak.
- `docs/performance.md` resume las pruebas de rendimiento y sus KPIs.
