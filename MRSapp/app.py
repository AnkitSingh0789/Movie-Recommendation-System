import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    overview = data['overview']
    release_date = data['release_date']
    rating = data['vote_average']
    return full_path, overview, release_date, rating

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_details = []
    for i in distances[1:11]:  # Start from 1 to skip the selected movie itself
        movie_id = movies.iloc[i[0]].movie_id  # Ensure you use the correct column name for the movie ID
        title = movies.iloc[i[0]].title
        poster, overview, release_date, rating = fetch_details(movie_id)
        recommended_movie_details.append((title, poster, overview, release_date, rating))
    return recommended_movie_details

# Load movies and similarity matrix
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
background_style = """
<style>
body {
background-image: url(https://www.google.com/url?sa=i&url=https%3A%2F%2Fgithub.com%2Ftopics%2Fmovie-recommender&psig=AOvVaw3SstWai0wA0B5b1LaeJ0SE&ust=1721229347069000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMDExf3sq4cDFQAAAAAdAAAAABAE);
background-size: cover;
}
</style>
"""
st.markdown(background_style, unsafe_allow_html=True)
st.markdown('<h1 class="title">Movie Recommendation System</h1>', unsafe_allow_html=True)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Recommendation button
if st.button('Recommend'):
    recommended_movies = recommend(selected_movie)
    st.markdown('<h2 class="subtitle">Recommended Movies</h2>', unsafe_allow_html=True)
    for title, poster, overview, release_date, rating in recommended_movies:
        st.markdown(f"### {title}")
        st.image(poster, width=150)
        st.markdown(f"**Release Date:** {release_date}")
        st.markdown(f"**Rating:** {rating}")
        st.markdown(f"**Overview:** {overview}")
        st.markdown("---")  # Divider line
    # Success and error messages
    st.success('We got the movies!', icon="✅")
