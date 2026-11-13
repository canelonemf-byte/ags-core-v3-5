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

class TestHybrixHealthAndLocalRead(unittest.TestCase):
    def setUp(self):
        main.DB_PATH = Path('/workspace/scratch/test_state_health.json')
        main.API_KEY = ''
        self.client = TestClient(main.app, client=('127.0.0.1', 12345))
        self.client.__enter__()
        main.app.state.db = {'projects_meta': {}, 'telemetry': [], 'predictions': []}

    def tearDown(self):
        self.client.__exit__(None, None, None)
        if main.DB_PATH.exists():
            main.DB_PATH.unlink()

    def test_health_ok_without_key(self):
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['service'], 'hybrix')

    def test_read_ok_from_localhost_without_key(self):
        res = self.client.get('/api/v1/hybrix/telemetry')
        self.assertEqual(res.status_code, 200)
        self.assertIn('items', res.json())

    def test_read_forbidden_from_non_loopback_without_key(self):
        with TestClient(main.app, client=('10.1.2.3', 12345)) as c:
            res = c.get('/api/v1/hybrix/telemetry')
            self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
