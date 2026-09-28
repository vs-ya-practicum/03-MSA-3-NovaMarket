import logging

from locust import HttpUser, between, task


logger = logging.getLogger(__name__)


class CircuitBreakerUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.circuit_breaker_activated = False

    @task
    def test_circuit_breaker(self):
        logger.info("Starting Circuit Breaker test...")

        response = self.client.get(
            "/logistics/?type=error",
            name="/logistics/?type=error",
        )
        if (
            response.status_code == 503
            and '"status": "fallback"' in response.text
            and not self.circuit_breaker_activated
        ):
            logger.warning("Circuit Breaker activated under load")
            self.circuit_breaker_activated = True
