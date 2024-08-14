import pickle
import streamlit as st
import requests

movies = pickle.load(open('Models/movies.pkl', 'rb'))
similarity = pickle.load(open('Models/similarity.pkl', 'rb'))
movie_list = movies['title'].values

HOME_IMAGE = "Image/Banner.jpg"


def recommend(selected_movie):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch Poster From API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=5dc569a32ec52b70d17cea7fe0bc1dd3'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']


def HomePage():
    st.header("Movie Recommendation System")
    st.image(HOME_IMAGE)
    st.markdown(
        """
        **Using the NLP to build the recommendation system**

        ### About Me
        **<i class="fa fa-user"></i> Name:** Nasif Azam\n
        **<i class="fa fa-envelope"></i> Email:** nasifazam07@gmail.com\n
        **<i class="fa fa-mobile-alt"></i> Phone:** +880-1533903305\n
        **<i class="fa fa-map-marker-alt"></i> Address:** Mirpur, Dhaka, Bangladesh

        <a href="https://www.facebook.com/md.nasif850" target="_blank" style="margin-right: 10px;"><i class="fab fa-facebook fa-2x"></i></a>
        <a href="https://github.com/Nasif-Azam" target="_blank" style="margin-right: 10px; color:black;"><i class="fab fa-github fa-2x"></i></a> 
        <a href="https://www.linkedin.com/in/nasif-azam-9aa2331a0/" target="_blank" style="margin-right: 10px; color:sky;"><i class="fab fa-linkedin fa-2x"></i></a> 
        <a href="https://www.hackerrank.com/profile/Nasif_Azam" target="_blank" style="margin-right: 10px; color:green;"><i class="fab fa-hackerrank fa-2x"></i></a> 
        <a href="https://www.kaggle.com/nasifazam" target="_blank" style="margin-right: 10px; color:blue;"><i class="fab fa-kaggle fa-2x"></i></a>  

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True
    )


def AboutPage():
    st.header("About Project")
    st.markdown("""
     ### Dataset
     Given that major films costing over $100 million to produce can still flop, this question is more important than ever to the industry. 
     Film aficionados might have different interests. 
     This is a great place to start digging in to those questions, with data on the plot, cast, crew, budget, and revenues of several thousand films. 
     ### Data Source
     We (Kaggle) have removed the original version of this dataset per a DMCA takedown request from IMDB. 
     In order to minimize the impact, we're replacing it with a similar set of films and data fields from The Movie Database (TMDb) in accordance with their terms of use. 
     The bad news is that kernels built on the old dataset will most likely no longer work. You can port your existing kernels over with a bit of editing. This kernel offers functions and examples for doing so. You can also find a general introduction to the new format here. The new dataset contains full credits for both the cast and the crew, rather than just the first three actors.
     ### Content
     - **tmdb_5000_credits.csv:** 4 Columns
     - **tmdb_5000_movies.csv:** 20 Columns
     ### Acknowledgements
    This dataset was generated from The Movie Database API. This product uses the TMDb API but is not endorsed or certified by TMDb.
    Their API also provides access to data on many additional movies, actors and actresses, crew members, and TV shows. You can try it for yourself here.    

""", unsafe_allow_html=True)


def RecommendationPage():
    st.header('Movie **:green[Recommendation]** System')
    selected_movie_name = st.selectbox(
        'Type or select your **:green[preferable movie]** from the dropdown :sunglasses:',
        movie_list
    )

    if st.button('Show Recommendation'):
        names, posters = recommend(selected_movie_name)
        col1, col2, col3, col4 = st.columns(4)  # Define 4 columns

        # First row
        with col1:
            st.markdown(names[0])
            st.image(posters[0])
        with col2:
            st.markdown(names[1])
            st.image(posters[1])
        with col3:
            st.markdown(names[2])
            st.image(posters[2])
        with col4:
            st.markdown(names[3])
            st.image(posters[3])

        # Second row
        col5, col6, col7, col8 = st.columns(4)  # Define another 4 columns for the second row

        with col5:
            st.markdown(names[4])
            st.image(posters[4])
        with col6:
            st.markdown(names[5])
            st.image(posters[5])
        with col7:
            st.markdown(names[6])
            st.image(posters[6])
        with col8:
            st.markdown(names[7])
            st.image(posters[7])
        st.balloons()


st.set_page_config(
    page_title="Movie Recommendation",
    page_icon="🎥",
    layout='wide',
    menu_items={
        'Get Help': 'https://github.com/Nasif-Azam',
        'Report a bug': 'mailto:nasifazam07@gmail.com',
        'About': "### Movie Recommendation System.\nThis app recommend similar movies using NLP (Cosine Similarity)."
    }
)

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select Page:", ["Home", "About Project", "Recommendations"])

if app_mode == "Home":
    HomePage()
elif app_mode == "About Project":
    AboutPage()
else:
    RecommendationPage()

