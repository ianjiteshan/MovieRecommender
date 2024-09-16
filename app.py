import pickle
import streamlit as st
import requests


# Fetch the movie poster using the provided TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            full_path = "https://via.placeholder.com/500x750?text=No+Image+Available"  # Fallback if no image
        return full_path
    except Exception as e:
        st.error(f"Error fetching movie poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


# Recommendation system that returns both movie names and posters
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []

        # Get top 5 recommended movies
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error recommending movies: {e}")
        return [], []


# Streamlit app interface
st.header('Movie Recommender System')

# Load the pickled data
try:
    movies = pickle.load(open('movies_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {e}")

# Dropdown for movie selection
if 'movies' in locals():
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

# Button to display recommendations
if st.button('Show Recommendation'):
    if selected_movie:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        if recommended_movie_names:
            # Dynamic column layout to display up to 5 recommendations
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if idx < len(recommended_movie_names):
                    with col:
                        st.text(recommended_movie_names[idx])
                        st.image(recommended_movie_posters[idx])
        else:
            st.error("No recommendations available.")
    else:
        st.error("Please select a movie.")
