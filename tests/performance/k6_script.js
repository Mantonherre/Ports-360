import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 10,
  duration: '30m',
  thresholds: {
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const host = __ENV.CONTEXT_ADAPTER_HOST || 'http://localhost:8010';
  const payload = JSON.stringify([{ id: 'soak', value: Math.random() }]);
  const params = { headers: { 'Content-Type': 'application/json' } };
  const res = http.post(`${host}/events/ingest`, payload, params);
  check(res, { 'accepted': (r) => r.status === 202 });
}
