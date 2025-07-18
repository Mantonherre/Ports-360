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

The Context Adapter is routed through Traefik under the `/api` prefix.
Traefik removes this prefix before forwarding requests, so the service
exposes endpoints like `/health`, `/metrics` or `/events/ingest` normally.
