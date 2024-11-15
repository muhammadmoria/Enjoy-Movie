import joblib
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Enhanced CSS Styling with Stickers and Improved Layout
st.markdown("""
    <style>
        /* Background and General Layout */
        body {
            background: linear-gradient(135deg, #141E30, #243B55);
            color: #E0E0E0;
            font-family: 'Roboto', sans-serif;
        }

        /* Main Title with Sticker */
        .main-title {
            font-size: 2.8em;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        }

        /* Section Title Styling */
        .section-title {
            font-size: 1.8em;
            color: #FFD700;
            font-weight: bold;
            margin-top: 15px;
            text-align: center;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }

        /* Card Styling */
        .card {
            background: #6B8E23;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: scale(1.02);
        }

        /* Feedback and Input Fields */
        .feedback-box {
            background: #2F2F3B;
            color: #E0E0E0;
            padding: 5px;
            border-radius: 8px;
            border: 1px solid #FFD700;
            margin-bottom: 10px;
        }

        /* Input Field Styling */
        .stTextInput > div, .stTextArea > div {
            background-color: #333945;
            color: #FFFFFF;
            border-radius: 5px;
            border: 1px solid #FFD700;
            padding: 5px;
        }

        /* Responsive Buttons with Stickers */
        .stButton>button {
            background-color: #FFD700;
            color: #2C3E50;
            font-size: 1.1em;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            position: relative;
            padding-left: 35px;
        }
        .stButton>button::before {
            content: "✨";
            position: absolute;
            left: 10px;
            top: 3px;
            font-size: 1.2em;
        }
        .stButton>button:hover {
            background-color: #FFC300;
            color: #282C34;
        }

        /* Uniform Recommendation Boxes */
        .recommend-box {
            background: #333945;
            color: #FFD700;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            margin: 5px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        }
        .recommend-box img {
            border-radius: 5px;
            height: 180px;
            width: 100%;
            object-fit: contain;
        }

        /* Footer */
        .footer {
            font-size: 14px;
            color: #95A5A6;
            margin-top: 20px;
            text-align: center;
            font-style: italic;
        }

        /* Mobile Adjustments */
        @media (max-width: 768px) {
            .main-title { font-size: 2.2em; }
            .section-title { font-size: 1.6em; }
        }
    </style>
""", unsafe_allow_html=True)

# Main Title with Icon
st.markdown("""<div class="main-title">🎬 AI-Powered Movie Recommendations Engine </div>""", unsafe_allow_html=True)

# Home Tab with About Me, Project Overview, and Technologies Used
tab1, tab2, tab3 = st.tabs(["🏠 Home", "📋 Recommender", "💬 Feedback"])

with tab1:
    st.markdown("""
        <div class="card">
            <h3 class="section-title">👤 About Me</h3>
            <p>
                Hi! I'm Muhammad Dawood, a data scientist specializing in machine learning, deep learning, and NLP.
                My passion lies in building intelligent systems and web applications that enhance user experiences.
            </p>
        </div>

        <div class="card">
            <h3 class="section-title">🚀 Project Overview</h3>
            <p>
                This AI-driven movie recommendation system uses advanced machine learning and NLP to suggest movies 
                based on user preferences. The model is trained on a vast dataset to deliver personalized recommendations.
            </p>
        </div>

        <div class="card">
            <h3 class="section-title">⚙️ Technologies Used</h3>
            <ul style="list-style: none; padding-left: 10px;">
                <li>🐍 <b>Python</b> - Programming Language</li>
                <li>🤖 <b>Machine Learning</b> - Recommendation Engine</li>
                <li>📊 <b>Data Science</b> - Data Processing and Analysis</li>
                <li>🧠 <b>Deep Learning</b> - Model Improvement</li>
                <li>💡 <b>NLP</b> - Natural Language Processing for Recommendations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            <p>Contact: <b>muhammaddawoodmoria@gmail.com</b> | Phone: <b>+923709152202</b></p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            <p>Github UserName: <b>muhammadmoria</b> | linkedin: muhammaddawood361510306</b></p>
        </div>
    """, unsafe_allow_html=True)





# Recommender Tab with Full Image Display
with tab2:
    st.markdown("""<div class="card">🎬 Discover Your Next Favorite Film </div>""", unsafe_allow_html=True)

    # Functions for poster fetching and recommendations
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

    # Load Data
    movies = joblib.load(open('movie_list.pkl', 'rb'))
    similarity = joblib.load(open('similarity_compressed.pkl', 'rb'))
    selected_movie = st.selectbox("Choose a Movie 🎥", movies['title'].values)

    # Show Recommendations
    if st.button('🎬 Show Recommendations'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.markdown(f"""
                <div class="recommend-box">
                    <img src="{poster}" alt="{name}">
                    <p><b>{name}</b></p>
                </div>
            """, unsafe_allow_html=True)

# Feedback Tab with Styled Input Fields and Feedback Display
with tab3:
    st.markdown("<div class='card'>💬 We Value Your Feedback!</div>", unsafe_allow_html=True)

    name = st.text_input("Name", key="name_input")
    feedback = st.text_area("Message", key="feedback_input")

    if st.button("🚀 Submit Feedback"):
        if name and feedback:
            with open("feedback.txt", "a") as f:
                f.write(f"{datetime.now().date()} - {name}: {feedback}\n")
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please provide both name and feedback.")

    # Display previous feedback in styled boxes
    st.markdown("<div class='card'>📜 Previous Feedback</div>", unsafe_allow_html=True)
    try:
        with open("feedback.txt", "r") as f:
            for line in f.readlines():
                st.markdown(f"<div class='feedback-box'>{line}</div>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("No feedback has been provided yet.")
