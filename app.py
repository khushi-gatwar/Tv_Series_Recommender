import pickle
import streamlit as st
import requests
import pandas as pd 

def recommend(movie,num):
    index = tv_series[tv_series['name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overview = []
    recommended_movie_genres = []
    for i in distances[1:num+1]:
        recommended_movie_posters.append("https://image.tmdb.org/t/p/w500" + tv_series['poster_path'].iloc[i[0]])
        recommended_movie_names.append(tv_series['name'].iloc[i[0]])
        recommended_movie_overview.append(tv_series['overview'].iloc[i[0]])
        recommended_movie_genres.append(tv_series['genres'].iloc[i[0]])


    return recommended_movie_names,recommended_movie_posters,recommended_movie_overview,recommended_movie_genres

def ratingBased(genres,lang,rating = 6,num = 10):
  mov = tv_series[(tv_series['vote_average'] > rating) & (tv_series['genres'].str.contains(pat = genres.lower())) & (tv_series['original_language'] == lang.lower())]
  mov.loc[:, 'poster_path'] = "https://image.tmdb.org/t/p/w500" + mov['poster_path']
  #mov['poster_path'] = "https://image.tmdb.org/t/p/w500" + mov['poster_path']
  movie_list = mov['name'].head(num).tolist()
  mov_poster = mov['poster_path'].head(num).tolist()
  movie_overview = mov['overview'].head(num).tolist()
  movie_genres = mov['genres'].head(num).tolist()
  return movie_list,mov_poster,movie_overview,movie_genres


st.set_page_config(layout="wide")

st.header('Tv-Series Recommender System')
tv_series = pd.read_csv('tv_series.csv')
from sklearn.feature_extraction.text import TfidfVectorizer
tfid = TfidfVectorizer(stop_words= 'english')
from sklearn.metrics.pairwise import cosine_similarity
tfid_matrix = tfid.fit_transform(tv_series['tags'])
similarity = cosine_similarity(tfid_matrix, tfid_matrix)
#similarity = pickle.load(open('similarity.pkl','rb'))

category = ['--Select--','Rating & Categories: Metadata Based','Tv-Series: Content Based']
recommended_type = st.selectbox("Select your Preferred recommendation type",options=category)

if(recommended_type == category[0]):
    st.warning('Please select Recommendation Type!!')

elif(recommended_type == category[1]):
    genres = tv_series['genres'].unique()
    lang = ['english','hindi','spanish','japanese','korean','german','french']

    selected_genre = st.selectbox("Select your preferred genre",genres)
    selected_lang = st.selectbox("Select Language",lang)
    rating = st.slider("Select minimum rating",0,10,6)
    num = st.slider("Select number of recommendations",0,20,5)

    items_per_column = 3
    num_columns = num // items_per_column + (num % items_per_column > 0)

    # Iterate through data and display in columns

    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters,recommended_movie_overview,recommended_movie_genres = ratingBased(selected_genre,selected_lang,rating,num)

        
        for i in range(num_columns):
            with st.container():
                for j in range(items_per_column * i, min(items_per_column * (i + 1), len(recommended_movie_names))):
                    st.write(f"<div style='text-align: left; font-size: 20px;'> {recommended_movie_names[j]}</div>", unsafe_allow_html=True)
                    st.markdown("")
                    st.write("About: ",recommended_movie_overview[j])
                    st.write("Genre: ",recommended_movie_genres[j])
                    st.markdown("")
                    st.image(recommended_movie_posters[j],width=300)
                    st.markdown("<hr style='border-top: dashed 2px;'>", unsafe_allow_html=True)

            if i < num_columns - 1:
                st.markdown("")


elif recommended_type == category[2]:

    movie_list = tv_series['name'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )
    nums = st.slider('Select number of recommendations',0,50,5)

    items_per_column = 3
    num_columns = nums // items_per_column + (nums % items_per_column > 0)

    # Iterate through data and display in columns

    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters,recommended_movie_overview,recommended_movie_genres = recommend(selected_movie,nums)

        
        for i in range(num_columns):
            with st.container():
                for j in range(items_per_column * i, min(items_per_column * (i + 1), len(recommended_movie_names))):
                    st.write(f"<div style='text-align: left; font-size: 20px;'> {recommended_movie_names[j]}</div>", unsafe_allow_html=True)
                    st.markdown("")
                    st.write("About: ",recommended_movie_overview[j])
                    st.write("Genre: ",recommended_movie_genres[j])
                    st.markdown("")
                    st.image(recommended_movie_posters[j],width=300)
                    st.markdown("<hr style='border-top: dashed 2px;'>", unsafe_allow_html=True)

            if i < num_columns - 1:
                st.markdown("")
        

