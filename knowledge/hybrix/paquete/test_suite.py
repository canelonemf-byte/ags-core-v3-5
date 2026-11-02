import unittest
from pathlib import Path
import os
import pytest
from fastapi.testclient import TestClient
import main

class TestHybrixSystem(unittest.TestCase):
    def setUp(self):
        main.DB_PATH = Path('/workspace/scratch/test_state.json')
        main.API_KEY = 'test-secret-key'
        self.client = TestClient(main.app)
        self.client.__enter__()
        main.app.state.db = {'projects_meta': {}, 'telemetry': [], 'predictions': []}

    def tearDown(self):
        self.client.__exit__(None, None, None)
        if main.DB_PATH.exists():
            main.DB_PATH.unlink()

    def test_status_endpoint(self):
        res = self.client.get('/api/v1/hybrix/status')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 'online')

    def test_auth_rejection(self):
        res = self.client.post('/api/v1/hybrix/telemetry', json={'trial_id': 1, 'node_id': 'n1', 'viability': 0.9, 'active_electrodes': 10})
        self.assertEqual(res.status_code, 401)

    def test_telemetry_post_and_alert(self):
        headers = {'X-API-Key': 'test-secret-key'}
        res = self.client.post('/api/v1/hybrix/telemetry', json={'trial_id': 101, 'node_id': 'n1', 'viability': 0.65, 'active_electrodes': 8}, headers=headers)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['alert'], 'CRITICAL_LOW_VIABILITY')

if __name__ == '__main__':
    unittest.main()
