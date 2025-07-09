```mermaid
flowchart LR
  Sim[Sensor Simulator] -->|MQTT| Broker((Mosquitto))
  Broker --> ContextAdapter
```
