#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


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
    data = {
        'USERNAME': username,
        'USER_IMAGE': user_image,
        'TIMESTAMP': timestamp,
        'CONTENT': content,
        'POST_IMAGE': post_image,
    }
    html_file_name = "display_post"
    create_component(data, html_file_name)


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
