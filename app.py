import joblib
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Add responsive CSS styling
st.markdown("""
    <style>
        /* Responsive Main Title */
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Adjust font sizes for small devices */
        @media (max-width: 768px) {
            .main-title { font-size: 2em; }
            .section-title { font-size: 1.5em; }
            .intro-title { font-size: 2em; }
            .content { font-size: 0.9em; }
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
        .section-content {
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
        /* Mobile Responsive Tabs */
        .stTabs > div { display: flex; flex-direction: column; }
        /* Footer */
        .footer {
            font-size: 14px;
            color: #95A5A6;
            margin-top: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# App title and introduction
st.markdown("""# 📽️ Welcome to the AI-Powered Movie Recommendation System! 🚀 """)

# Responsive tabs for navigation
tab1, tab2, tab3 = st.tabs(["🏠Home", "📋Movie Recommender", "✍️ Provide Feedback"])

# Page 1: Home
with tab1:
    st.markdown("""
        ## 👋 About Me  
        Hi! I'm Muhammad Dawood, a data scientist with expertise in machine learning, deep learning, and Natural Language Processing (NLP).  
        I specialize in building intelligent systems, web applications, and crafting data-driven solutions for impactful user experiences.

        ## 🔍 Project Overview  
        This project is focused on recommending movies based on users' preferences and watching patterns.
        - **Data Collection** 📊: Processed and analyzed a diverse movie dataset.
        - **Intelligent Recommendations** 🔍: Leveraged machine learning algorithms to provide personalized recommendations.
        - **Model Optimization** 📈: Tuned model parameters for better accuracy.
        - **Deployment** 🌐: Developed a user-friendly app interface for easy navigation.
    """)

with tab2:
    st.markdown("Discover your next favorite film with our intelligent recommendation engine. 🎬✨")

    # Functions for fetching poster and recommending movies
    def fetch_poster(movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters

    st.header('🎬 Movie Recommender System 📽️')
    
    # Load data
    movies = joblib.load(open('movie_list.pkl', 'rb'))
    similarity = joblib.load(open('similarity_compressed.pkl', 'rb'))

    # Dropdown for selecting a movie
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

    # Show recommendations when the button is clicked
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        # Display recommendations with responsive columns
        cols = st.columns([1, 1, 1, 1, 1] if st.session_state.get("wide") else [1, 1, 1])

        for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
            with cols[i % len(cols)]:
                st.text(name)
                st.image(poster, use_column_width=True)

with tab3:
    st.title("💬 Provide Feedback")
    st.write("We value your feedback! Please share your experience with this app.")

    # Feedback form
    name = st.text_input("Name", "")
    feedback = st.text_area("Feedback", "")
    submit_feedback = st.button("Submit Feedback")

    if submit_feedback and name and feedback:
        with open("feedback.txt", "a") as f:
            f.write(f"{datetime.now().date()} - {name}: {feedback}\n")
        st.success("Thank you for your feedback!")
    elif submit_feedback:
        st.warning("Please enter both your name and feedback.")

    # Display previous feedback
    st.subheader("Previous Feedback")
    try:
        with open("feedback.txt", "r") as f:
            for line in f.readlines():
                st.write(line)
    except FileNotFoundError:
        st.info("No feedback has been provided yet.")
