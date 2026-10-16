import unittest

from app import app


class PortalRouteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cloud Support Portal", response.data)

    def test_health_endpoint_returns_json(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["application"], "cloud-support-portal")
        self.assertIn("checks", payload)

    def test_ops_endpoint_does_not_publish_secrets(self):
        response = self.client.get("/ops")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertNotIn("password", payload)
        self.assertNotIn("credentials", payload)


if __name__ == "__main__":
    unittest.main()
