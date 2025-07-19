# SmartPort Dashboard

Development:

```bash
npm install
npm run dev
```

The app will be available at http://localhost:5173.

Set `VITE_API_BASE` to the backend URL (e.g. `http://localhost:8000`) to enable
API calls from the dashboard. When `VITE_WS_ENDPOINT` is defined, the dashboard
will connect to that WebSocket endpoint for live data; otherwise it falls back
to local fake data.

### Static assets

Additional files placed under `public/` are copied verbatim to the production
build directory. This repository includes an `ads.txt` placeholder so requests
to `/ads.txt` do not trigger `404` errors in the web server logs.
