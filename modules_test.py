#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from unittest.mock import patch
import matplotlib.pyplot as plt
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Import for display_post
from unittest.mock import patch, MagicMock
import requests

# Write your tests below

'''class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    @patch("modules.requests.get")
    def test_create_valid_post(self, mock_get):
        # Mock a successful image request
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'image/png'}

        # Valid input data
        username = "test_user"
        user_image = "https://example.com/user.png"
        timestamp = "2025-03-12 10:00:00"
        content = "This is a test post."
        post_image = "https://example.com/post.png"

        # Call the function
        display_post(username, user_image, timestamp, content, post_image)

        # Assertions (mocked request should have been called)
        mock_get.assert_called_with(post_image, stream=True, timeout=5)
    
    @patch('modules.requests.get')
    @patch('modules.st.warning')
    @patch('modules.st.session_state', new_callable=lambda: type('SessionStateMock', (object,), {})())
    @patch('modules.st.markdown')
    def test_display_post_invalid_image(self, mock_markdown, mock_session_state, mock_warning, mock_requests_get):
        """Test display_post with an invalid image URL."""
        mock_requests_get.side_effect = requests.RequestException("Error")

        display_post("TestUser", "invalid_url", "2025-03-12", "Test content", "invalid_url")

        mock_warning.assert_called_with("Invalid image URL. Your post will be created without an image.")
        mock_markdown.assert_called()
    
    @patch('modules.st.markdown')
    def test_display_post_handles_none_values(self, mock_markdown):
        """Test display_post with None values."""
        display_post(None, None, None, None, None)
        mock_markdown.assert_called()

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""
    
    #ChatGPT helped write the syntax for these tests 
    def test_function_runs_without_error(self):
        sample_workouts = [
        {"start_timestamp": "2025-03-01 08:00", "end_timestamp": "2025-03-01 09:00", "distance": 5, "steps": 6000, "calories_burned": 400},
        {"start_timestamp": "2025-03-02 08:30", "end_timestamp": "2025-03-02 09:15", "distance": 7.2, "steps": 8000, "calories_burned": 550},
        ]
        try:
            display_activity_summary(sample_workouts)
        except Exception as e:
            self.fail(f"Function raised an exception {e} unexpectedly!")

    @patch('streamlit.dataframe')
    @patch('streamlit.pyplot')
    def test_table_renders(self, mock_pyplot, mock_dataframe):
        """Test that the summary table is rendered using placeholders for the Streamlit environment"""
        sample_workouts = [
            {"start_timestamp": "2025-03-01 08:00", "end_timestamp": "2025-03-01 09:00", "distance": 5, "steps": 6000, "calories_burned": 400},
            {"start_timestamp": "2025-03-02 08:30", "end_timestamp": "2025-03-02 09:15", "distance": 7.2, "steps": 8000, "calories_burned": 550},
        ]
        display_activity_summary(sample_workouts)  
        mock_dataframe.assert_called_once()  # Ensure dataframe is called

    @patch('streamlit.dataframe')
    @patch('streamlit.pyplot')
    def test_graph_renders(self, mock_pyplot, mock_dataframe):
        """Test that the graph is rendered using placeholders for the Streamlit environment"""
        sample_workouts = [
            {"start_timestamp": "2025-03-01 08:00", "end_timestamp": "2025-03-01 09:00", "distance": 5, "steps": 6000, "calories_burned": 400},
            {"start_timestamp": "2025-03-02 08:30", "end_timestamp": "2025-03-02 09:15", "distance": 7.2, "steps": 8000, "calories_burned": 550},
        ]
        display_activity_summary(sample_workouts)
        mock_pyplot.assert_called_once()  # Ensure plot is called'''


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_display_correctly(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the image, timestamp, and content are displayed correctly."""
        mock_get_genai_advice.return_value = {
            'timestamp': "2024-01-01 00:00:00",
            'content': "You're doing great!",
            'image': "https://example.com/image.jpg"
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_called_once_with(image)
        mock_subheader.assert_called_once_with(" :blue[2024-01-01 00:00:00]", divider="green")
        mock_title.assert_called_once_with(" :red[You're doing great!]")

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_empty_content(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the function handles empty content correctly."""
        mock_get_genai_advice.return_value = {
            'timestamp': "2024-01-01 00:00:00",
            'content': "",
            'image': "https://example.com/image.jpg"
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_called_once_with(image)
        mock_subheader.assert_any_call(" :blue[2024-01-01 00:00:00]", divider="green")
        mock_title.assert_any_call(" :red[]")

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_none_inputs(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the function handles None inputs correctly."""
        mock_get_genai_advice.return_value = {
            'timestamp': None,
            'content': None,
            'image': "https://example.com/image.jpg"
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_called_once_with(image)
        mock_subheader.assert_any_call(" :blue[No timestamp available]", divider="green")
        mock_title.assert_any_call(" :red[No motivational message available]")

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_invalid_image_url(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the function handles invalid image URLs gracefully."""
        mock_get_genai_advice.return_value = {
            'timestamp': "2024-01-01 00:00:00",
            'content': "Test content.",
            'image': "invalid_url"
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_called_once_with(image)
        mock_subheader.assert_any_call(" :blue[2024-01-01 00:00:00]", divider="green")
        mock_title.assert_any_call(" :red[Test content.]")

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_none_image(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the function handles None image correctly."""
        mock_get_genai_advice.return_value = {
            'timestamp': "2024-01-01 00:00:00",
            'content': "Motivational message",
            'image': None
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_not_called()
        mock_subheader.assert_called_once_with(" :blue[2024-01-01 00:00:00]", divider="green")
        mock_title.assert_any_call(" :red[Motivational message]")
        mock_title.assert_any_call(" :red[No image available]")

    @patch("streamlit.image")
    @patch("streamlit.subheader")
    @patch("streamlit.title")
    @patch("modules.get_genai_advice")
    def test_none_timestamp(self, mock_get_genai_advice, mock_title, mock_subheader, mock_image):
        """Tests that the function handles None timestamp correctly."""
        mock_get_genai_advice.return_value = {
            'timestamp': None,
            'content': "Motivational message",
            'image': "https://example.com/image.jpg"
        }
        mock_data = mock_get_genai_advice.return_value
        timestamp = mock_data['timestamp']
        content = mock_data['content']
        image = mock_data['image']

        display_genai_advice(timestamp, content, image)

        mock_get_genai_advice.assert_called_once_with('user1')
        mock_image.assert_called_once_with(image)
        mock_subheader.assert_called_once_with(" :blue[No timestamp available]", divider="green")
        mock_title.assert_called_once_with(" :red[Motivational message]")




class TestDataFetcher(unittest.TestCase):

    def test_get_user_workouts_valid_user(self):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        mock_row = MagicMock()
        mock_row.workout_id = "workout1"
        mock_row.start_timestamp = "2024-07-29 07:00:00"
        mock_row.end_timestamp = "2024-07-29 08:00:00"
        mock_row.StartLocationLat = 37.7749
        mock_row.StartLocationLong = -122.4194
        mock_row.EndLocationLat = 37.8049
        mock_row.EndLocationLong = -122.4210
        mock_row.distance = 5.0
        mock_row.steps = 8000
        mock_row.calories_burned = 400

        mock_query_job.result.return_value = [mock_row]

        expected_result = [{
            'workout_id': "workout1",
            'start_timestamp': "2024-07-29 07:00:00",
            'end_timestamp': "2024-07-29 08:00:00",
            'start_lat_lng': (37.7749, -122.4194),
            'end_lat_lng': (37.8049, -122.4210),
            'distance': 5.0,
            'steps': 8000,
            'calories_burned': 400,
        }]

        result = get_user_workouts(mock_client, "user1")
        self.assertEqual(result, expected_result)

    def test_get_user_workouts_no_workouts(self):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job

        result = get_user_workouts(mock_client, "user_unknown")
        self.assertEqual(result, [])

    def test_get_user_workouts_multiple_workouts(self):
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        row1 = MagicMock()
        row1.workout_id = "workout1"
        row1.start_timestamp = "2024-07-29 07:00:00"
        row1.end_timestamp = "2024-07-29 08:00:00"
        row1.StartLocationLat = 37.7749
        row1.StartLocationLong = -122.4194
        row1.EndLocationLat = 37.8049
        row1.EndLocationLong = -122.4210
        row1.distance = 5.0
        row1.steps = 8000
        row1.calories_burned = 400

        row2 = MagicMock()
        row2.workout_id = "workout2"
        row2.start_timestamp = "2024-07-30 09:00:00"
        row2.end_timestamp = "2024-07-30 10:00:00"
        row2.StartLocationLat = 40.7128
        row2.StartLocationLong = -74.0060
        row2.EndLocationLat = 40.7308
        row2.EndLocationLong = -73.9976
        row2.distance = 6.5
        row2.steps = 10000
        row2.calories_burned = 500

        mock_query_job.result.return_value = [row1, row2]

        result = get_user_workouts(mock_client, "user1")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['workout_id'], "workout1")
        self.assertEqual(result[1]['workout_id'], "workout2")

if __name__ == "__main__":
    unittest.main()
