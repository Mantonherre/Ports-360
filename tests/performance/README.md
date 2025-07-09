# Pruebas de rendimiento

Este directorio contiene los scripts utilizados para las pruebas de carga de SmartPort.

## Locust

`locustfile.py` define tres grupos de usuarios:
- 30 usuarios publican en `/events/ingest` con cargas aleatorias de 1 a 3 KB.
- 30 usuarios consultan `/entities/{t}/{id}` para obtener un acierto de caché.
- 20 usuarios mantienen una suscripción WebSocket a `entity_update`.

Ejemplo de ejecución:

```bash
locust -f tests/performance/locustfile.py --headless -u 80 -r 80 -t 2m --host http://localhost:8010
```

## k6

`k6_script.js` ejecuta una prueba de tipo *soak* durante 30 minutos con 10
usuarios virtuales enviando un mensaje cada 500 ms.

```bash
k6 run tests/performance/k6_script.js
```

## pgbench

Para estresar la base de datos TimescaleDB se incluye `pgbench.sh` que lanza
100 000 transacciones con 10 hilos.

```bash
./tests/performance/pgbench.sh
```
