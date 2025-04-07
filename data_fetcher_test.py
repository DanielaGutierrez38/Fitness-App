#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from google.cloud import bigquery
import os
import datetime
import pytz
import sys
from data_fetcher import get_user_sensor_data, get_genai_advice, load_dotenv, vertexai
from vertexai.generative_models import GenerativeModel
from data_fetcher import _vertexai_initialized

class MockGenerativeModel:
    def __init__(self, expected_message, *args, **kwargs):
        self.expected_message = expected_message

    def generate_content(self, *args, **kwargs):
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].text.strip.return_value = self.expected_message
        return mock_response

class TestDataFetcher(unittest.TestCase):

    def setUp(self):
        global _vertexai_initialized
        _vertexai_initialized = False

    """Tests for get_user_sensor_data_success, these tests were created with help from Gemini"""
    @patch('google.cloud.bigquery.Client')
    def test_get_user_sensor_data_success(self, mock_bigquery_client):
        """Tests successful retrieval of user sensor data."""

        mock_query_job = MagicMock()
        mock_results = [
            {'sensor_type': 'accelerometer', 'timestamp': '2024-01-01 00:00:00', 'data': 10.5},
            {'sensor_type': 'gyroscope', 'timestamp': '2024-01-01 00:01:00', 'data': 20.2},
        ]
        mock_query_job.result.return_value = mock_results

        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertEqual(result, mock_results)
        mock_bigquery_client.assert_called_once()
        mock_client.query.assert_called_once()
        query = mock_client.query.call_args[0][0]
        self.assertIn(user_id, query)
        self.assertIn(workout_id, query)

    @patch('google.cloud.bigquery.Client')
    @patch('builtins.print')
    def test_get_user_sensor_data_error(self, mock_print, mock_bigquery_client):
        """Tests handling of BigQuery errors."""

        mock_bigquery_client.side_effect = Exception("BigQuery error")

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch('google.cloud.bigquery.Client')
    def test_empty_result(self, mock_bigquery_client):
        """Tests handling of empty results from BigQuery."""

        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []

        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertEqual(result, [])
        mock_bigquery_client.assert_called_once()

    @patch('google.cloud.bigquery.Client')
    def test_data_type_handling(self, mock_bigquery_client):
        """Tests handling of different data types from BigQuery."""

        mock_query_job = MagicMock()
        mock_results = [
            {'sensor_type': 'temperature', 'timestamp': '2024-01-01 00:00:00', 'data': 36.5},
            {'sensor_type': 'heart_rate', 'timestamp': '2024-01-01 00:01:00', 'data': 80},
            {'sensor_type': 'pressure', 'timestamp': '2024-01-01 00:02:00', 'data': "1013.25"},
        ]
        mock_query_job.result.return_value = mock_results

        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertEqual(result, mock_results)

    @patch('google.cloud.bigquery.Client')
    def test_partial_data(self, mock_bigquery_client):
        """Tests handling of rows with missing columns."""

        mock_query_job = MagicMock()
        mock_results = [
            {'sensor_type': 'accelerometer', 'timestamp': '2024-01-01 00:00:00'},
            {'sensor_type': 'gyroscope', 'data': 20.2},
        ]
        mock_query_job.result.return_value = mock_results

        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertEqual(result, mock_results)
    
    @patch('google.cloud.bigquery.Client')
    def test_large_dataset_handling(self, mock_bigquery_client):
        """Tests handling of a large dataset from BigQuery."""

        large_dataset = [{'sensor_type': 'test', 'timestamp': '2024-01-01 00:00:00', 'data': 1.0} for _ in range(1000)]

        mock_query_job = MagicMock()
        mock_query_job.result.return_value = large_dataset

        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        user_id = "test_user"
        workout_id = "test_workout"

        result = get_user_sensor_data(user_id, workout_id)

        self.assertEqual(result, large_dataset)
    
    """Tests for get_genai_advice, these tests were created with help from Gemini"""
    
    @patch('data_fetcher.vertexai.init')
    @patch('os.environ.get')
    @patch('random.choice')
    @patch('random.randint')
    @patch('data_fetcher.datetime')  # Patch the 'datetime' module in data_fetcher
    @patch('data_fetcher.GenerativeModel')
    @patch('data_fetcher.get_user_workouts')
    def test_get_genai_advice_success(self, mock_get_user_workouts, mock_generative_model, mock_datetime_module, mock_randint, mock_choice, mock_os_environ_get, mock_vertexai_init):
        from data_fetcher import get_genai_advice

        mock_os_environ_get.side_effect = lambda key, default=None: {
        "PROJECT_ID": "test_project",  # Assuming this is for your project ID
        "TIMEZONE": "America/New_York", # Replace "TIMEZONE" with the actual env var name
        # Add other environment variables your function might use
        }.get(key, default)

        mock_choice.return_value = 'https://test.image.com'
        mock_randint.return_value = 12345

        # Create a mock datetime class with a mock now() method
        mock_datetime_class = MagicMock()
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-01-01 12:00:00 "
        mock_datetime_class.now.return_value = mock_now
        mock_datetime_module.datetime = mock_datetime_class

        expected_message = "Stay strong!"
        mock_generative_model.return_value = MockGenerativeModel(expected_message)

        # Configure the return value for the mocked get_user_workouts
        mock_get_user_workouts.return_value = [
            {"workout_id": 1, "name": "Running", "duration": 30, "date": "2025-04-01"},
            {"workout_id": 2, "name": "Weightlifting", "sets": 3, "reps": 10, "date": "2025-04-03"},
        ]

        result = get_genai_advice("test_user")

        self.assertEqual(result['advice_id'], 12345)
        self.assertEqual(result['content'], expected_message)
        self.assertEqual(result['image'], 'https://test.image.com')
        self.assertEqual(result['timestamp'], "2024-01-01 12:00:00 ")
        #mock_vertexai_init.assert_called_once_with(project="test_project", location="us-central1")
        mock_datetime_class.now.assert_called_once()
        mock_get_user_workouts.assert_called_once_with("test_user") # Assert that get_user_workouts was called

    @patch('data_fetcher.vertexai.init')
    @patch('random.choice')
    @patch('data_fetcher.datetime')  # Patch the 'datetime' module in data_fetcher
    @patch('data_fetcher.GenerativeModel')
    @patch('google.cloud.bigquery.Client')
    def test_get_genai_advice_none_image(self,mock_bigquery_client, mock_generative_model, mock_datetime_module, mock_choice, mock_vertexai_init):
        from data_fetcher import get_genai_advice

        mock_choice.return_value = None

        # Create a mock datetime class with a mock now() method
        mock_datetime_class = MagicMock()
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-01-01 12:00:00 "
        mock_datetime_class.now.return_value = mock_now
        mock_datetime_module.datetime = mock_datetime_class  # Set the datetime attribute of the mocked module

        expected_message = "Keep going!"
        mock_generative_model.return_value = MockGenerativeModel(expected_message)
        mock_bigquery_client.return_value = MagicMock()

        result = get_genai_advice("test_user")
        self.assertEqual(result['image'], None)
        self.assertEqual(result["content"], expected_message)
        self.assertEqual(result['timestamp'], "2024-01-01 12:00:00 ")
        mock_datetime_class.now.assert_called_once()
        mock_vertexai_init.assert_called_once_with(project=None, location="us-central1")
    
if __name__ == "__main__":
    unittest.main()
