#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Import for display_post
from unittest.mock import patch

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    @patch("streamlit.markdown")
    def test_display_post(self, mock_markdown):
        """Tests that display_post correctly calls Streamlit markdown with expected HTML."""
        username = "John Doe"
        user_image = "https://example.com/user.jpg"
        timestamp = "2025-03-12 10:00:00"
        content = "This is a test post."
        post_image = "https://example.com/post.jpg"

        display_post(username, user_image, timestamp, content, post_image)

        # Check if Streamlit markdown is called with HTML that contains user_image and post_image
        html_call_args = " ".join(str(arg) for arg in mock_markdown.call_args[0])
        
        self.assertIn(user_image, html_call_args)
        self.assertIn(post_image, html_call_args)
        self.assertIn(username, html_call_args)
        self.assertIn(content, html_call_args)
        self.assertIn(timestamp, html_call_args)
    
    @patch("streamlit.markdown")
    def test_display_post_empty_content(self, mock_markdown):
        """Tests display_post with an empty content field."""
        username = "Jane Doe"
        user_image = "https://example.com/jane.jpg"
        timestamp = "2025-03-12 12:00:00"
        content = ""
        post_image = "https://example.com/post2.jpg"

        display_post(username, user_image, timestamp, content, post_image)

        html_call_args = " ".join(str(arg) for arg in mock_markdown.call_args[0])
        
        self.assertIn(user_image, html_call_args)
        self.assertIn(post_image, html_call_args)
        self.assertIn(username, html_call_args)
        self.assertIn(timestamp, html_call_args)
        self.assertNotIn("This is a test post.", html_call_args)  # Ensure previous content is not mistakenly included
    
    @patch("streamlit.markdown")
    def test_display_post_long_content(self, mock_markdown):
        """Tests display_post with a long content field."""
        username = "Alice"
        user_image = "https://example.com/alice.jpg"
        timestamp = "2025-03-12 15:00:00"
        content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5  # Long content
        post_image = "https://example.com/post3.jpg"

        display_post(username, user_image, timestamp, content, post_image)

        html_call_args = " ".join(str(arg) for arg in mock_markdown.call_args[0])
        
        self.assertIn(user_image, html_call_args)
        self.assertIn(post_image, html_call_args)
        self.assertIn(username, html_call_args)
        self.assertIn(timestamp, html_call_args)
        self.assertIn("Lorem ipsum", html_call_args)  # Ensure part of the long content appears
    
    @patch("streamlit.markdown")
    def test_display_post_null_values(self, mock_markdown):
        """Tests display_post with None values for all fields."""
        display_post(None, None, None, None, None)
        html_call_args = " ".join(str(arg) for arg in mock_markdown.call_args[0])
        
        self.assertNotIn("None", html_call_args)  # Ensure None values are not displayed as text
    
    @patch("streamlit.markdown")
    def test_display_post_invalid_image_urls(self, mock_markdown):
        """Tests display_post with invalid image URLs."""
        username = "Bob"
        user_image = "not_a_valid_url"
        timestamp = "2025-03-12 16:00:00"
        content = "Testing invalid images."
        post_image = "also_not_a_valid_url"

        display_post(username, user_image, timestamp, content, post_image)

        html_call_args = " ".join(str(arg) for arg in mock_markdown.call_args[0])
        
        self.assertNotIn("not_a_valid_url", html_call_args)  # Ensure invalid URLs are not included

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
