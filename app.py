# import streamlit as st
# import pickle
# import pandas as pd
# import requests


# # Load the movies DataFrame
# movies = pickle.load(open('movies.pkl', 'rb'))

# # Load the similarity matrix
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_movies_poster=[]
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
        
#         recommended_movies.append(movies.iloc[i[0]].title)
#         #fetch poster from APIS
#         recommended_movies_poster.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_poster

# # Get the list of movie titles
# movies_list = movies['title'].values

# st.title('Movie Recommender System')

# selected_movie_name = st.selectbox(
#     'Select a movie:',
#     movies_list)

# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])
   
import streamlit as st
import pickle
import pandas as pd
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import time

# Load the movies DataFrame
movies = pickle.load(open('movies.pkl', 'rb'))

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except (ConnectionError, Timeout) as e:
            st.warning(f"Connection error occurred: {e}. Retrying...")
            time.sleep(2)  # Wait before retrying
        except RequestException as e:
            st.error(f"An error occurred: {e}")
            break
    return "https://via.placeholder.com/500"  # Return a placeholder image if all retries fail

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Get the list of movie titles
movies_list = movies['title'].values

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    
        
