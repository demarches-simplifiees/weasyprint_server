from unittest import TestCase
from pathlib import Path
from weasyprint_server.app import create_app

PORT = 8000


class TestIntegrations(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"BASE_URL": f"http://localhost:{PORT}/"}).test_client()

    def test_ping(self):
        response = self.app.get(
            "/ping",
        )
        self.assertEqual(response.status_code, 200)

    def test_ping_maintenance(self):
        # on touch a file maintenance
        maintenance = Path("maintenance")
        maintenance.touch()

        response = self.app.get(
            "/ping",
        )
        self.assertEqual(response.status_code, 404)

        maintenance.unlink()
