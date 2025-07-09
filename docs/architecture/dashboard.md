```mermaid
graph TD
  sensor_sim -->|MQTT| context_adapter
  context_adapter -->|WS entity_update| Dashboard
  Dashboard --> User
  timeseries_writer --> Postgres
```
