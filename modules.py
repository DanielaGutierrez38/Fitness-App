#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)

# Function partially created by Copilot with "implement display_post to look like the image: (insert Mockup of display_post)"
def display_post(username, user_image, timestamp, content, post_image):
    """Displays a post with the given details.

    Args:
        username (str): The username of the person who made the post.
        user_image (str): The URL or path to the user's profile image.
        timestamp (str): The time when the post was made.
        content (str): The content of the post.
        post_image (str): The URL or path to the image associated with the post.
    """
    post = {
        "timestamp": timestamp,
        "post_image": post_image,
        "username": username,
        "content": content,
        "user_image": user_image
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


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
