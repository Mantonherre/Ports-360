import pytest

from services.timeseries.app.main import metrics


@pytest.mark.asyncio
async def test_metrics_endpoint():
    response = await metrics()
    assert response.status_code == 200
    body = response.body.decode()
    assert "mqtt_messages_total" in body
