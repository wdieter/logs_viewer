import unittest
from unittest.mock import patch, MagicMock
from service import app


class TestHandleGetLogs(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("domain.get_logs")
    def test_handle_get_logs_success(self, mock_get_logs):
        # mock the get_logs function to return a fake log
        mock_log = MagicMock()
        mock_log.to_dict.return_value = {"file_name": "system.log", "logs": ["log entry 1", "log entry 2"]}
        mock_get_logs.return_value = [mock_log]

        # perform a GET request with valid parameters
        response = self.app.get("/logs?filename=system.log&n=2&keyword=error")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("logs", data)
        self.assertEqual(len(data["logs"]), 1)
        self.assertEqual(data["logs"][0]["file_name"], "system.log")

    def test_handle_get_logs_invalid_n(self):
        # Test with an invalid 'n' parameter
        response = self.app.get("/logs?filename=system.log&n=-1")
        data = response.get_json()

        # Assert error response for invalid 'n' parameter
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], 'Parameter "n" must be a non-negative integer.')

    @patch("domain.get_logs", side_effect=FileNotFoundError)  # mock get_logs to raise a FileNotFoundError
    def test_handle_get_logs_file_not_found(self, mock_get_logs):
        response = self.app.get("/logs?filename=nonexistentfile")
        data = response.get_json()

        # assert error response for file not found
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "file not found")

