import streamlit as st
import pickle
import requests
from config import TMDB_API_KEY


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender")
selected_val = st.selectbox("Select a movie name from dropdown", movies_list)


def recommend(movie_name_input: str):
    id = movies[movies['title'] == movie_name_input].index[0]
    distance = sorted(
        list(enumerate(similarity[id])), reverse=True, key=lambda vector: vector[1])
    recommended_list = []
    recommended_posters = []
    for i in distance[0:5]:
        movie_id = movies.iloc[i[0]].id
        recommended_list.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_list, recommended_posters


if st.button("Show Recommend movies like this"):
    movies_name, movies_poster = recommend(selected_val)
    cols = st.columns(5, gap='medium')  # Create columns
    for i in range(5):
        with cols[i]:
            st.text(movies_name[i])
            st.image(movies_poster[i],  use_container_width=True)
