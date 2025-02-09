import pickle
import streamlit as st
import requests

import json 
from streamlit_lottie import st_lottie 
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🎬 My Movie Guru",
    page_icon="🍿",
    layout="wide"
    )
st.markdown("""
    <style>
        
        .st-emotion-cache-z5fcl4 {
            width: 100%;
            padding: 2rem 5rem 10rem!important;
            min-width: auto;
            max-width: initial;
        }
         p>code{
              color:green;
              font-weight:bold;
              font-size:18px;
          }         
        div.st-emotion-cache-1v0mbdj img:hover{
            cursor:pointer;
            transform:scale(1.1);
           }
        h2#movies-recommendation-system{
            text-align:center;
            color:cyan !important;
            font-size:42px;
            border:3px solid red;
            border-radius:20px;
        }
        h2#movies-recommendation-system .st-emotion-cache-10trblm{
            text-shadow:2px -2px  red !important;
        }

        .st-emotion-cache-1y4p8pa{
            padding:2rem 0.5rem ;
        }
       
       

        
            
    </style>

""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    vote_average=data['vote_average']
    poster_path = data['poster_path']
    overview = data['overview']
    runtime = data['runtime']
    genres = data['genres']
    adult = data['adult']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,vote_average,overview,runtime,genres,adult

# def fetch_vote(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     vote_average=data['vote_average']
#     return vote_average
def fetch_genres(genres):
    print(genres)
    l = len(genres)
    s_str="| "
    if l>=1:
        for i in range(l):
            print(genres[i]["name"])
            s_str+=genres[i]["name"]+" | "
    print(s_str)
    return s_str

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_vote = []
    recommended_overview=[]
    recommended_runtime=[]
    recommended_genres=[]
    recommended_adult=[]
    for i in distances[1:11]:
        # fetch the movie poster
        
        movie_id = movies.iloc[i[0]].movie_id
        poster,vote,overview,runtime,genres,adult = fetch_poster(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_vote.append(vote)
        recommended_overview.append(overview) 
        recommended_runtime.append(runtime)
        recommended_genres.append(genres)
        recommended_adult.append(adult)

    return recommended_movie_names,recommended_movie_posters,recommended_vote,recommended_overview,recommended_runtime,recommended_genres, recommended_adult


col3,col1, col2= st.columns([0.25,0.15,0.8],gap="large")

with col1:
     
    path = "logo.json"
    with open(path,"r") as file: 
        url = json.load(file) 


    st_lottie(url, 
        reverse=True, 
        height=140, 
        width=140, 
        speed=1, 
        loop=True, 
        quality='high', 
        key='Movie'
    )

      

with col2:
    st.title('🍿🎬 My Movie :red[_Guru_] 🎓')

    st.subheader('Smart Picks, Endless Flicks! 🎥')
    st.markdown("<h5>🎬 Discover your next favorite movie!</h5>",unsafe_allow_html=True)
    st.subheader("",divider="red")
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
st.markdown("<h5 styple='margin-top:20px;!important'>Type or select a film to find similar must-watch picks! 🍿✨</h5>",unsafe_allow_html=True)
selected_movie = st.selectbox(
    "",
    movie_list
)

# hero = st.empty()
# with hero.container():
#     path = "hero.json"
#     with open(path,"r") as file: 
#         url = json.load(file) 


#     st_lottie(url, 
#         reverse=True, 
#         height=540, 
#         width=540, 
#         speed=1, 
#         loop=True, 
#         quality='high', 
#         key='hero'
#     )

if st.button('Show Recommendation'):
    col1,col2,col3 = st.columns([0.33,0.30,0.15],gap="medium")
    with col2:
        p = st.empty()
        with p.container():
            path = "movie_loading.json"
            with open(path,"r") as file: 
                url = json.load(file) 


            st_lottie(url, 
                reverse=True, 
                height=240, 
                width=240, 
                speed=1, 
                loop=True, 
                quality='high', 
                key='loading'
            )
    
    recommended_movie_names,recommended_movie_posters,recommended_votes,recommended_overview,recommended_runtime,recommended_genres, recommended_adult = recommend(selected_movie)
    p.empty()
    st.subheader("",divider="red")
    #col1, col2, col3, col4, col5 = st.columns(5)
    cols1 = st.columns(5)    
    st.subheader("",divider="red")
    for i in range(5):
        
        if i<5 and i>=0 :
            with cols1[i]:
                
                #st.write(":red[**Movie**] "+recommended_movie_names[0])                    
                st.image(recommended_movie_posters[i])
                st.markdown(f"<p style='font-size:18px;overflow-x: auto;white-space: nowrap;'><strong>Movie :</strong> {recommended_movie_names[i]}</p>", unsafe_allow_html=True)
                st.write(":black[**Genres:**]",fetch_genres(recommended_genres[i]))
                st.write("**Duration:**",recommended_runtime[i]," Min",)
                st.write("**Rating:** ⭐ {:.1f}/10".format(recommended_votes[i]))
                st.markdown("<br>",unsafe_allow_html=True)
                
    cols2 = st.columns(5)
    st.subheader("",divider="red")
    for i in range(5,10):
        
        if i<10 and i>=5 :
            with cols2[i-5]:
                
                #st.write(":red[**Movie**] "+recommended_movie_names[0])                      
                st.image(recommended_movie_posters[i])
                st.markdown(f"<p style='font-size:18px;overflow-x: auto;white-space: nowrap;'><strong>Movie :</strong> {recommended_movie_names[i]}</p>", unsafe_allow_html=True)
                st.write(":black[**Genres:**]",fetch_genres(recommended_genres[i]))
                st.write("**Duration:**",recommended_runtime[i]," Min")
                st.write("**Rating:** ⭐ {:.1f}/10".format(recommended_votes[i]))   
                st.markdown("<br>",unsafe_allow_html=True)
                 
    # with col2:
    #     # st.text(recommended_movie_names[1])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[1]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[1])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[1]))

    # with col3:
    #     # st.text(recommended_movie_names[2])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[2]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[2])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[2]))
    # with col4:
    #     # st.text(recommended_movie_names[3])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[3]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[3])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[3]))
    # with col5:
    #     # st.text(recommended_movie_names[4])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[4]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[4])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[4]))

    # # st.markdown("""<hr style="margin:0;">""", unsafe_allow_html=True)
    # st.subheader("",divider="red")
    # col6, col7, col8, col9, col10 = st.columns(5)
    
    # with col6:
    #     # st.text(recommended_movie_names[5])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[5]}</p>", unsafe_allow_html=True)        
    #     st.image(recommended_movie_posters[5])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[5]))
    # with col7:
    #     # st.text(recommended_movie_names[6])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[6]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[6])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[6]))

    # with col8:
    #     # st.text(recommended_movie_names[7])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[7]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[7])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[7]))
    # with col9:
    #     # st.text(recommended_movie_names[8])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[8]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[8])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[8]))
    # with col10:
    #     # st.text(recommended_movie_names[9])
    #     st.markdown(f"<p style='font-size:16px;overflow-x: auto;white-space: nowrap;'>{recommended_movie_names[9]}</p>", unsafe_allow_html=True)
    #     st.image(recommended_movie_posters[9])
    #     st.text("Rating: ⭐ {:.1f}/10".format(recommended_votes[9]))
    # st.subheader("",divider="red")
    
        
else:
    col1,col2,col3 = st.columns([0.30,0.50,0.15],gap="medium")
    with col2:
        hero = st.empty()
        with hero.container():
            path = "hero.json"
            with open(path,"r") as file: 
                url = json.load(file) 

            st_lottie(url, 
                reverse=True, 
                height=540, 
                width=540, 
                speed=1, 
                loop=True, 
                quality='high', 
                key='hero2',
            )
       

st.markdown("""
     
    <p><strong>Devloped By Himanshu</strong></p>
    
    <p>Follow me on <img href="insta.png" style="width=28px"></p>
    </div>

""",unsafe_allow_html=True)
st.image("insta.png",width=28)





link_url = "https://www.instagram.com/himanshu_77_mahor/"
st.markdown(f'<a href="{link_url}">Click here for follow </a><hr>', unsafe_allow_html=True)



# import streamlit as st
# import streamlit_lottie

# with st.echo():
#     st.lottie("movie.json")

    
# import time
# import requests
# import json
# import streamlit as st
# from streamlit_lottie import st_lottie
# from streamlit_lottie import st_lottie_spinner


# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()


# lottie_url_hello = "movie.json"

# lottie_hello = "movie.json"

# st_lottie(lottie_hello, key="hello")







