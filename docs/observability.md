# Observabilidad

```mermaid
graph LR
  sensor_sim --> context_adapter
  context_adapter -->|metrics| Prometheus
  timeseries -->|metrics| Prometheus
  twin_core -->|metrics| Prometheus
  Prometheus --> Grafana
```
