# twin-core

GraphQL service for the 3D Digital Twin. It exposes an Apollo Server with a minimal schema and listens to entity updates via WebSocket.

This service is a stub used for integration tests. The Cesium 3D loader is simplified and a local Redis instance caches entity states.

## Development

```bash
npm install
npm run build
npm start
```
