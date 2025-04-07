#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts, display_sensor_data
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

# New imports
from datetime import datetime
from google.cloud import bigquery

# Created tabs and display post code by Copilot using the following prompt: "create a streamlit app that showcases a post. that post will have a timestamp, post_image, username, content (of the post), and user_image."
def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "GenAI Advice", "Activity Summary", "Recent Workouts", "Sensor Data", "Community"])
    userId = None # Example data

    with tab1:
        # An example of displaying a custom component called "my_custom_component"
        value = st.text_input('Enter your name')
        display_my_custom_component(value)

        # Get data
        userId = 'user3'
        posts = get_user_posts(userId)  # Fetch a list of posts
        for post in posts: # Show every post
            display_post(post["username"], post["user_image"], post["timestamp"], post["content"], post["image"])
        
    with tab2:
        advice = get_genai_advice(userId)
        #call method in modules that displays the genAI advice
        display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
    
    with tab3:
        # Fetch user workouts and display activity summary
        userId = 'user1'
        workouts = get_user_workouts(userId)  # Fetch workouts for the user
        display_activity_summary(workouts)  # Pass workouts to display activity summary

    with tab4:
        userId = 'user1'
        workouts = get_user_workouts(userId)
        display_recent_workouts(workouts)

    with tab5:
        userId = 'user1'
        sensor_data = get_user_sensor_data(userId, 'workout1')
        display_sensor_data(sensor_data)

    with tab6:
        client = bigquery.Client()
        

        def display_all_posts():
            """
            Displays all posts in the Streamlit app.
            """
            posts = get_user_posts(userId)
            if posts:
                for post in posts:
                    st.write(f"\n Whats on your mind: {post['user_id']} - {post['timestamp']}: {post['content']}")
                    image_url = post['image']
                if image_url and image_url.startswith("http"):
                    try:
                        st.image(image_url, width=150)
                    except Exception as e:
                        st.error(f"Error displaying image from URL: {e}")
                else:
                    st.write("Image not available.")

            else:
                st.write("No posts available.")

        def display_community_page(user_id):
            """
            Displays the community page for a given user.

            Args:
                user_id: The ID of the user.
            """
            genai_advice = get_genai_advice(user_id)
            user_profile = get_user_profile(user_id)

            if user_profile:
                st.write(f"User Profile: {user_profile['full_name']} (@{user_profile['username']})")
                st.image(user_profile['profile_image'], width=100)
                st.write("News Feed:")
                display_all_posts()
                st.write("\nAdvice & Encouragement:")
                if genai_advice:
                    st.write(f"Advice: {genai_advice['content']}")
                    st.image(genai_advice['image'], width=150)
                else:
                    st.write("No GenAI advice found.")
            else:
                st.write(f'user {user_id} not found')
        display_community_page(userId)

        #############################################################################
# activity_page.py
#
# This file displays a user’s activity (3 recent workouts, summary, and share button).
# Line written by ChatGPT (post generation logic & workout summary layout).
#############################################################################

import streamlit as st
from google.cloud import bigquery
from datetime import datetime
import pytz
import uuid

def get_recent_workouts(user_id, limit=3):
    client = bigquery.Client()
    query = """
        SELECT WorkoutId, StartTimestamp, EndTimestamp, TotalDistance, TotalSteps, CaloriesBurned
        FROM `keishlyanysanabriatechx25.bytemeproject.Workouts`
        WHERE UserId = @user_id
        ORDER BY StartTimestamp DESC
        LIMIT @limit
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )
    results = client.query(query, job_config=job_config).result()
    return [dict(row.items()) for row in results]

def get_activity_summary(user_id):
    client = bigquery.Client()
    query = """
        SELECT
            SUM(TotalDistance) AS total_distance,
            SUM(TotalSteps) AS total_steps,
            SUM(CaloriesBurned) AS total_calories
        FROM `keishlyanysanabriatechx25.bytemeproject.Workouts`
        WHERE UserId = @user_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    result = client.query(query, job_config=job_config).result()
    row = next(iter(result), {})
    return {
        'total_distance': row.get('total_distance', 0),
        'total_steps': row.get('total_steps', 0),
        'total_calories': row.get('total_calories', 0)
    }

def share_stat_as_post(user_id, stat_type="steps", value=None):
    if value is None:
        raise ValueError("Stat value is required.")

    client = bigquery.Client()

    messages = {
        "steps": f"Look at this, I walked {value} steps today!",
        "distance": f"I crushed it — {value} miles logged today!",
        "calories": f"Burned {value} calories! Progress feels good."
    }

    content = messages.get(stat_type, f"Today's achievement: {value} {stat_type}!")

    post_id = str(uuid.uuid4())
    timestamp = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")

    query = """
        INSERT INTO `keishlyanysanabriatechx25.bytemeproject.Posts` (PostId, AuthorId, Timestamp, Content)
        VALUES (@post_id, @user_id, @timestamp, @content)
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("post_id", "STRING", post_id),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("timestamp", "STRING", timestamp),
            bigquery.ScalarQueryParameter("content", "STRING", content),
        ]
    )

    client.query(query, job_config=job_config).result()
    return {"status": "success", "message": "Post shared!", "post_content": content}

def display_activity_page(user_id):
    st.subheader("Activity Summary")

    summary = get_activity_summary(user_id)
    st.metric("Total Steps", int(summary['total_steps']))
    st.metric("Total Distance (mi)", round(summary['total_distance'], 2))
    st.metric("Calories Burned", int(summary['total_calories']))

    st.subheader("Recent Workouts")
    workouts = get_recent_workouts(user_id)
    for w in workouts:
        st.write(f"Workout: {w['WorkoutId']}")
        st.write(f"Start: {w['StartTimestamp']}, End: {w['EndTimestamp']}")
        st.write(f"Distance: {w['TotalDistance']} mi, Steps: {w['TotalSteps']}, Calories: {w['CaloriesBurned']}")
        st.markdown("---")

    st.subheader("Share a Stat with the Community")
    stat = st.selectbox("Choose a stat to share:", ["steps", "distance", "calories"])
    if st.button("Share It!"):
        value = summary.get(f"total_{stat}")
        result = share_stat_as_post(user_id, stat, value)
        st.success(result["message"])
        st.write(f"📝 {result['post_content']}")


# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
