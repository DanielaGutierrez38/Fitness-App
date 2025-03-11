#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

# New imports
from datetime import datetime

userId = 'user1'

# Created tabs and display post code by Copilot using the following prompt: "create a streamlit app that showcases a post. that post will have a timestamp, post_image, username, content (of the post), and user_image."
def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    # Create tabs
    tab1, tab2 = st.tabs(["Home", "Posts"])

    with tab1:
        # An example of displaying a custom component called "my_custom_component"
        value = st.text_input('Enter your name')
        display_my_custom_component(value)
        
    with tab2:
        # Sample data
        post = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "post_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg",
            "username": "John Doe",
            "content": "This is a sample post content. Streamlit makes it easy to create beautiful apps.",
            "user_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
        }

        # Custom CSS for colored rows
        st.markdown(
            """
            <style>
            .post-container {
                border-radius: 10px; /* Rounded corners for the entire post */
                overflow: hidden; /* Ensure child elements respect the border radius */
                border: 1px solid #ddd; /* Optional: Add a border for better visibility */
            }
            .user-box {
                background-color: #4285F4; /* Google's blue color */
                padding: 10px;
            }
            .user-row {
                display: flex;
                align-items: center;
            }
            .user-row img {
                border-radius: 50%;
                margin-right: 10px;
                height: 50px; /* Set the height of the user image */
                width: 50px; /* Set the width of the user image */
                object-fit: cover; /* Prevent the image from stretching */
            }
            .timestamp-row {
                background-color: #FBBC05; /* Google's yellow color */
                padding: 10px;
                display: flex;
                justify-content: center; /* Center horizontally */
                align-items: center; /* Center vertically */
                height: 50px; /* Set a fixed height for vertical centering */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Post container with rounded corners
        st.markdown(
            f"""
            <div class="post-container">
                <div class="user-box">
                    <div class="user-row">
                        <img src="{post['user_image']}">
                        <h3>{post['username']}</h3>
                    </div>
                    <p>{post['content']}</p>
                </div>
                <img src="{post['post_image']}" style="width: 100%; height: auto;">
                <div class="timestamp-row">
                    <p>Posted on: {post['timestamp']}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
