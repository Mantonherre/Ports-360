sequenceDiagram
  participant Client
  participant Adapter
  participant MQTT
  Client->>Adapter: POST /events/ingest
  Adapter->>MQTT: publish JSON
  Client->>Adapter: GET /entities/{t}/{id}
  Adapter->>MQTT: subscribe
  MQTT-->>Adapter: last JSON
  Adapter-->>Client: entity JSON
