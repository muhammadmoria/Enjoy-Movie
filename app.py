
import joblib
import streamlit as st
import requests
from  datetime import datetime


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)
# Add custom CSS for setting the background color to black
# Custom CSS for styling
st.markdown("""
    <style>
        /* Main Title */
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Section Titles */
        .section-title {
            font-size: 1.8em;
            color: #3498DB;
            font-weight: bold;
            margin-top: 30px;
            text-align: left;
        }
        /* Section Content */
        .section-content{
            text-align: center;
        }
        /* Home Page Content */
        .intro-title {
            font-size: 2.5em;
            color: #2C3E50;
            font-weight: bold;
            text-align: center;
        }
        .intro-subtitle {
            font-size: 1.2em;
            color: #34495E;
            text-align: center;
        }
        .content {
            font-size: 1em;
            color: #7F8C8D;
            text-align: justify;
            line-height: 1.6;
        }
        .highlight {
            color: #2E86C1;
            font-weight: bold;
        }
        /* Recommendation Titles and Descriptions */
        .recommendation-title {
            font-size: 22px;
            color: #2980B9;
        }
        .recommendation-desc {
            font-size: 16px;
            color: #7F8C8D;
        }
        /* Separator Line */
        .separator {
            margin-top: 10px;
            margin-bottom: 10px;
            border-top: 1px solid #BDC3C7;
        }
        /* Footer */
        .footer {
            font-size: 14px;
            color: #95A5A6;
            margin-top: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""# 📽️ Welcome to the AI-Powered Movie Recommendation System! 🚀 """)



tab1, tab2, tab3 = st.tabs(["🏠Home", "📋Movie Recommender", "✍️ Provide Feedback"])
# Page 1: Home
with tab1:
   st.markdown("""
        
        ## 👋 About Me  
        Hi! I'm Muhammad Dawood, a data scientist with expertise in machine learning, deep learning, and Natural Language Processing (NLP).  
        I specialize in building intelligent systems, web applications, and crafting data-driven solutions for impactful user experiences.

        ## 🔍 Project Overview  
        This project is focused on recommending movies based on users' preferences and watching patterns. Here’s what we’ve accomplished:
        - **Data Collection** 📊: Processed and analyzed a diverse movie dataset with feature engineering to capture meaningful attributes and user preferences.
        - **Intelligent Recommendations** 🔍: Leveraged powerful machine learning algorithms to provide personalized movie recommendations based on similarity scores and user input.
        - **Model Optimization** 📈: Tuned model parameters to improve recommendation accuracy, ensuring the system adapts effectively to diverse movie tastes.
        - **Deployment** 🌐: Developed an intuitive app interface that is user-friendly, allowing easy navigation for discovering movies.

        ## 💻 Technologies Used  
        - **Languages & Libraries**: Python, Pandas, Scikit-Learn, Joblib, and Streamlit for an interactive interface.
        - **Deployment**: Built and deployed using Streamlit to offer a dynamic and engaging user experience.

        Created by Muhammad Dawood, combining machine learning and data engineering to enhance how we discover films. 🌐
        Gmail: muhammaddawoodmoria@gmail.com
        """)

with tab2:
    st.markdown("""Discover your next favorite film with our intelligent recommendation engine,
        tailored to help you find movies you'll love. 🎬✨""")
    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters

    # Streamlit header
    st.header('🎬 Movie Recommender System 📽️')

    # Load the pre-trained data
    movies = joblib.load(open('movie_list.pkl', 'rb'))
    similarity = joblib.load(open('similarity_compressed.pkl', 'rb'))

    # Dropdown for selecting a movie
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    # Show recommendations when the button is clicked
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        # Use columns for displaying the movie posters and names
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
with tab3:
    st.title("💬 Provide Feedback")
    st.write("We value your feedback! Please share your experience with this app.")

    # Feedback form
    name = st.text_input("Name", "")
    feedback = st.text_area("Feedback", "")
    submit_feedback = st.button("Submit Feedback")

    if submit_feedback and name and feedback:
        # Save feedback to a file
        with open("feedback.txt", "a") as f:
            f.write(f"{datetime.now().date()} - {name}: {feedback}\n")
        st.success("Thank you for your feedback!")
    elif submit_feedback:
        st.warning("Please enter both your name and feedback.")

    # Display previous feedback
    st.subheader("Previous Feedback")
    try:
        with open("feedback.txt", "r") as f:
            feedback_history = f.readlines()
            for line in feedback_history:
                st.write(line)
    except FileNotFoundError:
        st.info("No feedback has been provided yet.")
