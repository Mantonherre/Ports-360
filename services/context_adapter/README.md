# Context Adapter

Microservice that bridges the REST API and MQTT bus using NGSI-LD messages.

```bash
docker build -t context-adapter .
docker run -e MQTT_HOST=mqtt -p 8010:8010 context-adapter
```
