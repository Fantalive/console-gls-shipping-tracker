import unittest
import requests

from unittest.mock import patch

from backend.api import fetch_parcel_data_with_retry
from backend.config import config

class TestFetchParcelData(unittest.TestCase):
    @patch("requests.get")
    def test_successful_api_call(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status = lambda: None
        result = fetch_parcel_data_with_retry(config["base_url"], "123456", "12345")
        self.assertEqual(result["status"], "success")

    @patch("requests.get")
    def test_retry_on_failure(self, mock_get):
        mock_get.side_effect = requests.ConnectionError
        with self.assertRaises(Exception):
            fetch_parcel_data_with_retry(config["base_url"], "123456", "12345")
