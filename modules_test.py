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




class TestDisplayRecentWorkouts(unittest.TestCase):

    @patch("data_fetcher.get_user_workouts")
    def test_empty_workouts_list(self, mock_get_user_workouts):
        """Test when the workouts list is empty"""
        mock_get_user_workouts.return_value = []
        workouts = mock_get_user_workouts.return_value
        result = display_recent_workouts(workouts)
        self.assertIsNone(result)

    @patch("data_fetcher.get_user_workouts")
    def test_single_workout_entry(self, mock_get_user_workouts):
        """Test when there is a single workout"""
        mock_get_user_workouts.return_value = [{
            'workout_id': 'workout1',
            'start_timestamp': '2024-03-10 08:00:00',
            'end_timestamp': '2024-03-10 08:30:00',
            'start_lat_lng': (2.36, 4.0),
            'end_lat_lng': (1.5444, 4.1),
            'distance': 5.2,
            'steps': 6000,
            'calories_burned': 300
        }]
        workouts = mock_get_user_workouts.return_value
        result = display_recent_workouts(workouts)
        self.assertIsNone(result)

    @patch("data_fetcher.get_user_workouts")
    def test_multiple_workouts_sorted(self, mock_get_user_workouts):
        """Test multiple workouts sorted by timestamp"""
        mock_get_user_workouts.return_value = [
            {'workout_id': 'workout1', 'start_timestamp': '2024-03-10 08:00:00', 'end_timestamp': '2024-03-10 08:30:00',
             'start_lat_lng': (2.0, 4.0), 'end_lat_lng': (2.0, 4.1), 'distance': 5.2, 'steps': 6000, 'calories_burned': 300},
            {'workout_id': 'workout2', 'start_timestamp': '2024-03-11 09:00:00', 'end_timestamp': '2024-03-11 09:45:00',
             'start_lat_lng': (2.0, 4.0), 'end_lat_lng': (2.0, 4.1), 'distance': 3.0, 'steps': 4000, 'calories_burned': 250}
        ]
        workouts = mock_get_user_workouts.return_value
        display_recent_workouts(workouts)
        self.assertEqual(workouts[0]['workout_id'], 'workout2')  # Most recent should be first
        self.assertEqual(workouts[1]['workout_id'], 'workout1')  # Older should be second

    @patch("data_fetcher.get_user_workouts")
    def test_workouts_with_same_start_time(self, mock_get_user_workouts):
        """Test multiple workouts with the same timestamp"""
        mock_get_user_workouts.return_value = [
            {'workout_id': 'workout1', 'start_timestamp': '2024-03-11 09:00:00', 'end_timestamp': '2024-03-11 09:45:00',
             'start_lat_lng': (2.0, 4.0), 'end_lat_lng': (2.0, 4.1), 'distance': 3.0, 'steps': 4000, 'calories_burned': 250},
            {'workout_id': 'workout2', 'start_timestamp': '2024-03-11 09:00:00', 'end_timestamp': '2024-03-11 09:45:00',
             'start_lat_lng': (2.0, 4.0), 'end_lat_lng': (2.0, 4.1), 'distance': 4.0, 'steps': 5000, 'calories_burned': 300}
        ]
        workouts = mock_get_user_workouts.return_value
        display_recent_workouts(workouts)
        self.assertEqual(len(workouts), 2)
        self.assertEqual(workouts[0]['workout_id'], 'workout1')

    @patch("data_fetcher.get_user_workouts")
    def test_workout_with_zero_and_negative_values(self, mock_get_user_workouts):
        """Test workout with zero and negative values"""
        mock_get_user_workouts.return_value = [
            {'workout_id': 'workout1', 'start_timestamp': '2024-03-10 07:00:00', 'end_timestamp': '2024-03-10 07:30:00',
             'start_lat_lng': (2.0, 4.0), 'end_lat_lng': (2.0, 4.0), 'distance': 0, 'steps': 0, 'calories_burned': -100}
        ]
        workouts = mock_get_user_workouts.return_value
        display_recent_workouts(workouts)
        self.assertEqual(workouts[0]['distance'], 0)
        self.assertEqual(workouts[0]['steps'], 0)
        self.assertEqual(workouts[0]['calories_burned'], -100)

    @patch("data_fetcher.get_user_workouts")
    def test_large_number_of_workouts(self, mock_get_user_workouts):
        """Test function with a large number of workouts"""
        workouts = []
        for i in range(100):
            workouts.append({
                'workout_id': f'workout{i}',
                'start_timestamp': f'2024-03-{10 + i % 20:02} 07:00:00',
                'end_timestamp': f'2024-03-{10 + i % 20:02} 07:30:00',
                'start_lat_lng': (2.0, 4.0),
                'end_lat_lng': (2.0, 4.1),
                'distance': 5.0,
                'steps': 6000,
                'calories_burned': 300
            })
        mock_get_user_workouts.return_value = workouts
        workouts = mock_get_user_workouts.return_value
        display_recent_workouts(workouts)
        self.assertEqual(len(workouts), 100)

if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    unittest.main()
