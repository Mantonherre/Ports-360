```mermaid
graph LR
  MQTT((Mosquitto)) --> TSWriter
  TSWriter -->|INSERT| PG[(TimescaleDB + PostGIS)]
```
