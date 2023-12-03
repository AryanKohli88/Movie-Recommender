import streamlit as st
import pickle
import pandas as pd
import requests
import constants
api_key = constants.key

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index] # vector for this movie
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6] # taking fromindex 1 o 6 because most similar at ind. 0 is the movie itself
    recs = []
    recposters = []
    for i in movie_list:
        recs.append(movies.iloc[i[0]].title)
        poster = fetchposter(movies.iloc[i[0]].movie_id)
        recposters.append(poster)
    return recs , recposters

def fetchposter(movieid):
    resp = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movieid, api_key))
    data = resp.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

selectedMovie = st.selectbox('Name a movie', movies['title'].values)

if st.button("Recommend"):
    st.text("Since you like "+ selectedMovie + ", You might also like:")
    names, posters= recommend(selectedMovie)

    col1, col2,col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col1:
        st.header(names[1])
        st.image(posters[1])
    with col1:
        st.header(names[2])
        st.image(posters[2])
    with col1:
        st.header(names[3])
        st.image(posters[3])
    with col1:
        st.header(names[4])
        st.image(posters[4])