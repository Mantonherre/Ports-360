# Pruebas de rendimiento

Este documento describe los indicadores clave (KPIs) utilizados para evaluar el
rendimiento de SmartPort.

## KPIs

- **rps**: peticiones por segundo procesadas.
- **latency p50/p95**: latencias de la API en los percentiles 50 y 95.
- **WS msg loss**: mensajes perdidos en las suscripciones WebSocket.
- **TPS DB**: transacciones por segundo en la base de datos.

## Resultados

| Escenario              | rps antes | rps después | p95 antes | p95 después |
|------------------------|---------:|-----------:|---------:|-----------:|
| Locust API/WS          |          |            |          |            |
| k6 Soak                |          |            |          |            |
| pgbench                |          |            |          |            |

La tabla anterior debe completarse tras ejecutar `tools/tune/tune.sh` y
comparar los resultados antes y después del ajuste automático.
