import os
import json
import random
from locust import FastHttpUser, task, between, events
from websocket import create_connection


class APIUser(FastHttpUser):
    wait_time = between(1, 2)
    host = os.getenv("CONTEXT_ADAPTER_HOST", "http://localhost:8010")

    @task(3)
    def ingest_event(self):
        size = random.randint(1024, 3072)
        payload = [
            {"id": "device-%d" % random.randint(1, 100), "value": "x" * (size - 20)}
        ]
        self.client.post("/events/ingest", json=payload, name="POST /events/ingest")

    @task(3)
    def get_entity(self):
        self.client.get("/entities/Sensor/1", name="GET /entities/{t}/{id}")


class WSUser(FastHttpUser):
    wait_time = between(1, 1)
    ws_url = os.getenv("TWIN_CORE_WS", "ws://localhost:8030")

    def on_start(self):
        self.ws = create_connection(self.ws_url)
        try:
            self.ws.send(json.dumps({"action": "subscribe", "topic": "entity_update"}))
        except Exception:
            events.request_failure.fire(
                request_type="ws",
                name="connect",
                response_time=0,
                exception="subscribe_failed",
            )

    @task
    def listen(self):
        try:
            self.ws.recv()
            events.request_success.fire(
                request_type="ws", name="recv", response_time=0, response_length=0
            )
        except Exception as exc:
            events.request_failure.fire(
                request_type="ws", name="recv", response_time=0, exception=exc
            )

    def on_stop(self):
        if self.ws:
            self.ws.close()
