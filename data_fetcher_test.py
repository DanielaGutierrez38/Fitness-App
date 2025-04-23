import unittest
import json
from unittest.mock import patch, MagicMock
import os
import datetime
import pytz
from data_fetcher import get_user_sensor_data, get_genai_advice, load_dotenv, vertexai, get_user_profile, ai_call_for_planner
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

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_sensor_data_success(self, mock_bigquery_client):
        mock_query_job = MagicMock()
        mock_results = [
            {'sensor_type': 'accelerometer', 'timestamp': '2024-01-01 00:00:00', 'data': 10.5},
            {'sensor_type': 'gyroscope', 'timestamp': '2024-01-01 00:01:00', 'data': 20.2},
        ]
        mock_query_job.result.return_value = mock_results
        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        result = get_user_sensor_data("test_user", "test_workout")
        self.assertEqual(result, mock_results)
        mock_bigquery_client.assert_called_once()
        mock_client.query.assert_called_once()
        query = mock_client.query.call_args[0][0]
        self.assertIn("test_user", query)
        self.assertIn("test_workout", query)

    @patch('data_fetcher.bigquery.Client')
    @patch('builtins.print')
    def test_get_user_sensor_data_error(self, mock_print, mock_bigquery_client):
        mock_bigquery_client.side_effect = Exception("BigQuery error")
        result = get_user_sensor_data("test_user", "test_workout")
        self.assertIsNone(result)
        mock_print.assert_called_once()

    @patch('data_fetcher.bigquery.Client')
    def test_empty_result(self, mock_bigquery_client):
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        result = get_user_sensor_data("test_user", "test_workout")
        self.assertEqual(result, [])
        mock_bigquery_client.assert_called_once()

    @patch('data_fetcher.bigquery.Client')
    def test_data_type_handling(self, mock_bigquery_client):
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

        result = get_user_sensor_data("test_user", "test_workout")
        self.assertEqual(result, mock_results)

    @patch('data_fetcher.bigquery.Client')
    def test_partial_data(self, mock_bigquery_client):
        mock_query_job = MagicMock()
        mock_results = [
            {'sensor_type': 'accelerometer', 'timestamp': '2024-01-01 00:00:00'},
            {'sensor_type': 'gyroscope', 'data': 20.2},
        ]
        mock_query_job.result.return_value = mock_results
        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        result = get_user_sensor_data("test_user", "test_workout")
        self.assertEqual(result, mock_results)

    @patch('data_fetcher.bigquery.Client')
    def test_large_dataset_handling(self, mock_bigquery_client):
        large_dataset = [{'sensor_type': 'test', 'timestamp': '2024-01-01 00:00:00', 'data': 1.0} for _ in range(1000)]
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = large_dataset
        mock_client = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_bigquery_client.return_value = mock_client

        result = get_user_sensor_data("test_user", "test_workout")
        self.assertEqual(result, large_dataset)

    @patch('data_fetcher.vertexai.init')
    @patch('os.environ.get')
    @patch('random.choice')
    @patch('random.randint')
    @patch('data_fetcher.datetime')
    @patch('data_fetcher.GenerativeModel')
    @patch('data_fetcher.get_user_workouts')
    def test_get_genai_advice_success(self, mock_get_user_workouts, mock_generative_model, mock_datetime_module, mock_randint, mock_choice, mock_os_environ_get, mock_vertexai_init):
        from data_fetcher import get_genai_advice

        mock_os_environ_get.side_effect = lambda key, default=None: {
            "PROJECT_ID": "test_project",  
            "TIMEZONE": "America/New_York",
        }.get(key, default)
        mock_choice.return_value = 'https://test.image.com'
        mock_randint.return_value = 12345

        mock_datetime_class = MagicMock()
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-01-01 12:00:00 "
        mock_datetime_class.now.return_value = mock_now
        mock_datetime_module.datetime = mock_datetime_class

        expected_message = "Stay strong!"
        mock_generative_model.return_value = MockGenerativeModel(expected_message)
        mock_get_user_workouts.return_value = [
            {"workout_id": 1, "name": "Running", "duration": 30, "date": "2025-04-01"},
            {"workout_id": 2, "name": "Weightlifting", "sets": 3, "reps": 10, "date": "2025-04-03"},
        ]

        result = get_genai_advice("test_user")

        self.assertEqual(result['advice_id'], 12345)
        self.assertEqual(result['content'], expected_message)
        self.assertEqual(result['image'], 'https://test.image.com')
        self.assertEqual(result['timestamp'], "2024-01-01 12:00:00 ")
        mock_datetime_class.now.assert_called_once()
        mock_get_user_workouts.assert_called_once_with("test_user")


# Imports for get_user_posts testing
import unittest
from unittest.mock import Mock, patch, MagicMock
import datetime
from google.cloud import bigquery
import sys
import os
from data_fetcher import get_user_posts, get_user_workouts

# Partially created by Gemini, Claude, and ChatGPT: "Create unittests for get_user_posts"
class TestGetUserPosts(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(spec=bigquery.Client)
        self.client_patcher = patch('data_fetcher.bigquery.Client', return_value=self.mock_client)
        self.client_patcher.start()
        self.test_user_id = "user123"
        self.test_timestamp = datetime.datetime(2023, 10, 15, 12, 30, 45)

    def tearDown(self):
        self.client_patcher.stop()

    def _setup_mock_query_result(self, rows):
        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = iter(rows)
        self.mock_client.query.return_value = mock_query_job

    def test_get_user_posts_with_complete_data(self):
        mock_rows = [
            {'PostId': 'post1', 'AuthorId': self.test_user_id, 'Timestamp': self.test_timestamp, 'Content': 'Test post content', 'PostImageUrl': 'https://example.com/image.jpg', 'Username': 'testuser', 'UserImageUrl': 'https://example.com/user.jpg'},
            {'PostId': 'post2', 'AuthorId': self.test_user_id, 'Timestamp': self.test_timestamp, 'Content': 'Another test post', 'PostImageUrl': 'https://example.com/image2.jpg', 'Username': 'testuser', 'UserImageUrl': 'https://example.com/user.jpg'}
        ]
        self._setup_mock_query_result(mock_rows)
        result = get_user_posts(self.test_user_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['post_id'], 'post1')

    def test_get_user_posts_with_missing_fields(self):
        mock_rows = [{'PostId': 'post3', 'AuthorId': self.test_user_id, 'Timestamp': self.test_timestamp, 'Content': None, 'PostImageUrl': None, 'Username': 'testuser', 'UserImageUrl': 'https://example.com/user.jpg'}]
        self._setup_mock_query_result(mock_rows)
        result = get_user_posts(self.test_user_id)
        self.assertEqual(result[0]['content'], '')
        self.assertEqual(result[0]['image'], '')

    def test_get_user_posts_no_results(self):
        self._setup_mock_query_result([])
        result = get_user_posts(self.test_user_id)
        self.assertEqual(result, [])

    def test_get_user_posts_sql_injection_prevention(self):
        malicious_user_id = "user123' OR 1=1 --"
        self._setup_mock_query_result([])
        get_user_posts(malicious_user_id)
        query_arg = self.mock_client.query.call_args[0][0]
        self.assertIn(f"WHERE p.AuthorId = '{malicious_user_id}'", query_arg)

class TestGetUserWorkout(unittest.TestCase):
    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_valid_user(self, mock_bigquery_client):
        mock_client_instance = mock_bigquery_client.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [MagicMock(WorkoutId="workout1", StartTimestamp=datetime.datetime(2024, 7, 29, 7, 0, 0), EndTimestamp=datetime.datetime(2024, 7, 29, 8, 0, 0), StartLocationLat=37.7749, StartLocationLong=-122.4194, EndLocationLat=37.8049, EndLocationLong=-122.4210, TotalDistance=5.0, TotalSteps=8000, CaloriesBurned=400)]
        expected_result = [{'WorkoutId': "workout1", 'StartTimestamp': "2024-07-29T07:00:00", 'end_timestamp': "2024-07-29T08:00:00", 'start_lat_lng': (37.7749, -122.4194), 'end_lat_lng': (37.8049, -122.4210), 'distance': 5.0, 'steps': 8000, 'calories_burned': 400}]
        from modules import get_user_workouts
        self.assertEqual(get_user_workouts("user1"), expected_result)

class TestGetUserProfile(unittest.TestCase):
    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile_success(self, mock_bigquery_client):
        mock_row_data = ('user1', 'Remi', 'remi_the_rems', 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg', datetime.date(1990, 1, 1), ['user2', 'user3', 'user4'])
        mock_row = MagicMock(UserId=mock_row_data[0], Name=mock_row_data[1], Username=mock_row_data[2], ImageUrl=mock_row_data[3], DateOfBirth=mock_row_data[4], friends=mock_row_data[5])
        mock_result = MagicMock()
        mock_result.__iter__.return_value = iter([mock_row])
        mock_bigquery_client.return_value.query.return_value.result.return_value = mock_result
        result = get_user_profile("user1")
        self.assertEqual(result["full_name"], "Remi")

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_profile_not_found(self, mock_bigquery_client):
        mock_result = MagicMock()
        mock_result.__iter__.return_value = iter([])
        mock_result.__next__.side_effect = StopIteration
        mock_client = MagicMock()
        mock_client.query.return_value.result.return_value = mock_result
        mock_bigquery_client.return_value = mock_client
        result = get_user_profile("nonexistent_user")
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
