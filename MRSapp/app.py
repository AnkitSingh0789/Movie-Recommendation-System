import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse  # For encoding the movie title for URLs


# Function to fetch movie details using The Movie Database (TMDb) API
def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        overview = data['overview']
        release_date = data['release_date']
        rating = data['vote_average']
    except:
        st.error("Failed to fetch movie details. Please try again later.")
        return None, None, None, None

    return full_path, overview, release_date, rating


# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True,
                       key=lambda x: x[1])
    recommended_movie_details = []
    for i in distances[1:11]:  # Start from 1 to skip the selected movie itself
        movie_id = movies.iloc[i[
            0]].movie_id  # Ensure you use the correct column name for the movie ID
        title = movies.iloc[i[0]].title
        poster, overview, release_date, rating = fetch_details(movie_id)
        recommended_movie_details.append(
            (title, poster, overview, release_date, rating))
    return recommended_movie_details


# Load movies and similarity matrix
@st.cache_data
def load_data():
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_list)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity


movies, similarity = load_data()

# CSS for styling
page_bg_img = '''
<style>
body {
    background-image: linear-gradient(to bottom right, rgba(34,193,195,0.6), rgba(253,187,45,0.6)), url("https://repository-images.githubusercontent.com/275336521/20d38e00-6634-11eb-9d1f-6a5232d0f84f");
    background-size: cover;
    background-attachment: fixed;
    color: #f0f0f0; /* Light color for readability */
    font-family: 'Roboto', sans-serif; /* Modern font */
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

h1, h2, h3, h4, h5, h6 {
    color: #f5f5f5;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.stButton button {
    background-color: #22c1c3; /* Primary button color */
    color: white;
    border-radius: 12px;
    padding: 0.5em 1em;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    font-size: 16px;
    cursor: pointer;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    background-color: #1aa0a2;
}

.movie-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
    border-radius: 12px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    width: 100%;
    max-width: 400px; /* Added max-width for responsive cards */
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.movie-poster {
    border-radius: 8px;
    width: 100%;
    max-width: 250px;
    transition: transform 0.2s ease;
    margin-bottom: 15px;
    cursor: pointer;
}

.movie-poster:hover {
    transform: scale(1.05);
}

.movie-details {
    text-align: center;
    padding: 0 20px;
    max-width: 100%;
}

.movie-title {
    font-size: 1.5em;
    color: #333;
    margin-bottom: 0.5em;
}

.movie-overview {
    font-size: 1em;
    color: #555;
    margin-bottom: 1em;
}

.movie-info {
    font-size: 0.9em;
    color: #777;
    margin-top: 0.5em;
}

.recommendation-section {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    align-items: center;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
}

@media (min-width: 768px) {
    .recommendation-section {
        grid-template-columns: auto 1fr;
        padding: 20px;
    }

    .movie-card {
        flex-direction: row;
    }

    .movie-details {
        text-align: left;
    }
}

.recommendation-container {
    margin: 2em 0;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.sidebar-section {
    color: #f0f0f0;
    margin-bottom: 1em;
    padding: 1em;
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
}

.sidebar-section h3 {
    margin-top: 0;
    color: #ffdb58; /* Different color for emphasis */
}

.stTextInput, .stSelectbox {
    margin-bottom: 1em;
}

footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    color: #f0f0f0;
    text-align: center;
    padding: 1em 0;
}

</style>
'''

# Inject CSS with Streamlit
st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app
st.title("🎬 Movie Recommendation System")
st.write("## Select a movie you like and get recommendations")

# Sidebar for filters and additional features
st.sidebar.header("Customize Your Experience")

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.write("### Filter Recommendations")

# Rating filter
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Dropdown for selecting a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Choose a movie", movie_list)

# Button to get recommendations
if st.button('Recommend'):
    recommended_movies = recommend(selected_movie)

    # Filter recommendations based on minimum rating
    filtered_movies = [
        movie for movie in recommended_movies if movie[4] >= min_rating
    ]

    st.write("## Recommended Movies:")

    # Display recommended movies in a structured layout
    for title, poster, overview, release_date, rating in filtered_movies:
        # URL encode the movie title
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(title)}"

        st.markdown(f"""
            <div class="recommendation-container">
                <div class="recommendation-section">
                    <a href="{google_search_url}" target="_blank">
                        <img src="{poster}" class="movie-poster"/>
                    </a>
                    <div class="movie-details">
                        <h3 class="movie-title">{title}</h3>
                        <p class="movie-overview">{overview}</p>
                        <p class="movie-info"><strong>Release Date:</strong> {release_date}</p>
                        <p class="movie-info"><strong>Rating:</strong> {rating}/10</p>
                    </div>
                </div>
            </div>
            """,
                    unsafe_allow_html=True)

# Footer
st.markdown('''
    <footer>
        <p>© 2024 Movie Recommendation System | Created by Ankit Singh</p>
    </footer>
    ''',
            unsafe_allow_html=True)
