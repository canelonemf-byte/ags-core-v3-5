import unittest
import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Adjust path to import main
sys.path.insert(0, "/workspace/scratch")
import main

class TestHYBRIXCIPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main.API_KEY = "ci-secret-key"

    def setUp(self):
        main.app.state.db = {"projects_meta": {}, "telemetry": [], "predictions": []}

    def test_status_endpoint(self):
        with TestClient(main.app) as client:
            res = client.get("/api/v1/hybrix/status")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["status"], "online")

    def test_authentication_security(self):
        with TestClient(main.app) as client:
            headers = {"X-API-Key": "wrong-key"}
            payload = {"trial_id": 1, "node_id": "test", "viability": 0.95, "active_electrodes": 10}
            res = client.post("/api/v1/hybrix/telemetry", json=payload, headers=headers)
            self.assertEqual(res.status_code, 401)

    def test_critical_viability_alert(self):
        with TestClient(main.app) as client:
            headers = {"X-API-Key": "ci-secret-key"}
            payload = {"trial_id": 99, "node_id": "bio-node-1", "viability": 0.64, "active_electrodes": 12}
            res = client.post("/api/v1/hybrix/telemetry", json=payload, headers=headers)
            self.assertEqual(res.status_code, 201)
            body = res.json()
            self.assertEqual(body.get("alert"), "CRITICAL_LOW_VIABILITY")
            self.assertTrue("auto_export_file" in body)

    def test_batch_telemetry_flushing(self):
        with TestClient(main.app) as client:
            headers = {"X-API-Key": "ci-secret-key"}
            batch = {
                "items": [
                    {"trial_id": 1, "node_id": "node-a", "viability": 0.85, "active_electrodes": 20},
                    {"trial_id": 2, "node_id": "node-b", "viability": 0.90, "active_electrodes": 24}
                ]
            }
            res = client.post("/api/v1/hybrix/telemetry/batch", json=batch, headers=headers)
            self.assertEqual(res.status_code, 201)
            self.assertEqual(res.json()["inserted"], 2)

if __name__ == "__main__":
    unittest.main()
