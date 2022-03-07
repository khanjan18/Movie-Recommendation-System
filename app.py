import pickle
import streamlit as st
import pandas as pd
import requests
from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '83c52c49ddee44475891ab5d3a3e5a3d'
from tmdbv3api import Movie
tmdb_movie = Movie()

similarity = pickle.load(open('similarity.pkl','rb'))
final_data  = pickle.load(open('final_data_dict.pkl','rb'))

final_data = pd.DataFrame(final_data)
final_data['movie_title'] = final_data['movie_title'].str.title()

def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=83c52c49ddee44475891ab5d3a3e5a3d&language=en-US'.format(movie_id))
    movie_data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+movie_data['poster_path']

def get_cast_details(movie):
    input_movie_name = tmdb_movie.search(movie)
    movie_id = input_movie_name[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key=83c52c49ddee44475891ab5d3a3e5a3d&language=en-US'.format(movie_id))
    json_data = response.json()
    casts_names = []
    casts_poster = []
    casts_chars = []

    for i in range(0,9):
        casts_names.append(json_data['cast'][i]['name'])
        casts_poster.append('https://image.tmdb.org/t/p/w500/'+json_data['cast'][i]['profile_path'])
        casts_chars.append(json_data['cast'][i]['character'])

    return casts_chars, casts_names, casts_poster

def recommend(movie):
    movie_index = final_data[final_data['movie_title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []
    recommended_movies_posters = []

    for i in recommended_movies_list:
        result = tmdb_movie.search(final_data.iloc[i[0]].movie_title)
        movie_id = result[0].id
        recommended_movies.append(final_data.iloc[i[0]].movie_title)
        recommended_movies_posters.append(get_poster(movie_id))
    return recommended_movies, recommended_movies_posters

def get_input_movie_details(movie):
    input_movie_name = tmdb_movie.search(movie)
    input_movie_id = input_movie_name[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=83c52c49ddee44475891ab5d3a3e5a3d&language=en-US'.format(input_movie_id))
    json_data = response.json()
    title = json_data['original_title']
    overview = json_data['overview']
    poster = 'https://image.tmdb.org/t/p/w500/'+json_data['poster_path']

    genres = []
    for i in range(0,len(json_data['genres'])):
        genres.append(json_data['genres'][i]['name'])

    genres = " ".join([str(i) for i in genres])

    release_date = json_data['release_date']
    runtime = str(json_data['runtime'])+" Minutes"
    IMDB_Rating = json_data['vote_average']
    status = json_data['status']

    return title,overview, poster,genres,release_date, runtime, IMDB_Rating,status

with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

st.markdown("<div style='color: #fff;position: fixed;text-align: right;bottom: 20px;right: 20px;width: 100%;'>Created By Khanjan Purohit</div>", unsafe_allow_html = True)

st.title("MOVIE RECOMMENDATION SYSTEM")

st.markdown("<br>", unsafe_allow_html = True)

input_movie = st.selectbox(
    "Enter a Movie Name",
    final_data['movie_title'].values
)

if st.button("Search"):
    recommended_movies,recommended_movies_posters = recommend(input_movie)
    title,overview,poster,genres,release_date,runtime,IMDB_Rating,status = get_input_movie_details(input_movie)
    casts_chars,casts_names, casts_poster = get_cast_details(input_movie)

    col1, col2 = st.columns(2)
    col3, col4, col5, col6 = st.columns(4)
    col7, col8, col9, col10 = st.columns(4)
    container1 = st.container()
    container2 = st.container()
    container3 = st.container()
    container4 = st.container()
    container5 = st.container()
    container6 = st.container()

    with container1:
        with col1:
            st.markdown("<br>", unsafe_allow_html = True)
            st.image(poster)
            st.markdown("<br>", unsafe_allow_html = True)
            st.markdown("<br>", unsafe_allow_html = True)
            st.markdown("<div style='font-size: 25px; text-align: right;'> TOP CAST </div>",unsafe_allow_html = True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<span>TITLE : </span>"+f"<span>{title}</span>", unsafe_allow_html = True)
            st.markdown("Overview : "+f"<span>{overview}</span>", unsafe_allow_html = True)
            st.markdown("Genres : "+ f"<span>{genres}</span>", unsafe_allow_html = True)
            st.markdown("Release Date : "+f"<span>{release_date}</span>", unsafe_allow_html = True)
            st.markdown("Runtime : "+f"<span>{runtime}</span>", unsafe_allow_html = True)
            st.markdown("IMDB Rating : "+ f"<span>{str(IMDB_Rating)}</span>", unsafe_allow_html = True)
            st.markdown("Status : "+f"<span>{status}</span>", unsafe_allow_html = True)
            st.markdown("<br>", unsafe_allow_html=True)

    with container2:
        with col3:
            st.image(casts_poster[0])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[0]}</b></span>", unsafe_allow_html = True)
            st.markdown(f"<span style='font-size: 14px; '>{casts_chars[0]}</span>", unsafe_allow_html = True)
        with col4:
            st.image(casts_poster[1])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[1]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[1]}</span>", unsafe_allow_html=True)
        with col5:
            st.image(casts_poster[2])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[2]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[2]}</span>", unsafe_allow_html=True)
        with col6:
            st.image(casts_poster[3])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[3]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[3]}</span>", unsafe_allow_html=True)

    with container3:
        with col3:
            st.image(casts_poster[4])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[4]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[4]}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: left;font-size: 26px;'>RECOMMENDED MOVIES</div>",
                        unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col4:
            st.image(casts_poster[5])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[5]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[5]}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html = True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col5:
            st.image(casts_poster[6])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[6]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[6]}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col6:
            st.image(casts_poster[7])
            st.markdown(f"<span style='font-size: 18px;'><b>{casts_names[7]}</b></span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size: 14px;'>{casts_chars[7]}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    with container4:
        with col7:
            st.markdown(f"<span>{recommended_movies[0]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[0])
        with col8:
            st.markdown(f"<span>{recommended_movies[1]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[1])
        with col9:
            st.markdown(f"<span>{recommended_movies[2]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[2])
        with col10:
            st.markdown(f"<span>{recommended_movies[3]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[3])

    with container5:
        with col7:
            st.markdown(f"<span>{recommended_movies[4]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[4])
        with col8:
            st.markdown(f"<span>{recommended_movies[5]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[5])
        with col9:
            st.markdown(f"<span>{recommended_movies[6]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[6])
        with col10:
            st.markdown(f"<span>{recommended_movies[7]}</span>", unsafe_allow_html = True)
            st.image(recommended_movies_posters[7])