import streamlit as st
import pybase64
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.graph_objects as go
import dash_map as dm
import time_series as ts
from prophet import Prophet


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = pybase64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size:180%;
        background-color:#CDE5F3;
  
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('Images/background img.png')  

# Design horizontal bar
menu = ["Home", "Water Quality", "Time Series", "About us"]
selection = option_menu(None, ["Home", "Water Quality", "Time Series", 'About us'], 
    icons=['house', "bi bi-droplet", "bi bi-graph-up", 'bi bi-info-square'], 
    menu_icon="cast", default_index=0, orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#D3E2F7"},
        "icon": {"color": "#172d90", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#ECFFFF"},
        "nav-link-selected": {"background-color": "#7CC4F5"},
    })


data = pd.read_csv(r'data/df.csv')

 
if selection == "Home":
    st.markdown('')
    

elif selection == "Water Quality":
    st.subheader("Geospatial Data")

elif selection == "Time Series":
    st.subheader("Water quality over time")

else:
    st.subheader('')
    st.subheader("About Team")
    st.markdown(" ")
    mikey_pic = Image.open("Images/MIKEY.jpg")
    emeka_pic = Image.open("Images/EMEKA.jpeg")
    bodine_pic = Image.open("Images/bodine.jpeg")
    othuke_pic = Image.open("Images/Othuke.jpeg")
    joseph_pic = Image.open("Images/Joseph.jpeg")
    johnson_pic = Image.open("Images/Johnson.jpeg")
    samson_pic = Image.open("Images/Samson.jpg")
    david_pic = Image.open("Images/David.png")
    theresa_pic = Image.open("Images/Theresa.jpeg")
    ehi_pic = Image.open("Images/Ehi.jpg")
    hasan_pic = Image.open("Images/Hasan.jpeg")


    st.header("Bodine Mazibuko - Team Leader")
    bodine, text = st.columns((1,2))

    with bodine:
        st.image(bodine_pic)

    with text:
        st.write("""
            Project management, analytical reporting and research skills, data visualization, UIUX.""")
    
    st.header("Michael Ndirangu -  Data Engineer")
    mikey, text1 = st.columns((1,2))

    with mikey:
        st.image(mikey_pic)

    with text1:
        st.write("""
            Michael is well versed in creating ETL pipelines in AWS Cloud, Azure Cloud, as well as in on premise environment with python 
            """)

    st.header("Odimegwu David - Data Scientist")
    emeka, text2 = st.columns((1,2))
    
    with emeka:
        st.image(emeka_pic)

    with text2:
        st.write("""
            David's skills include machine learning, SQL, and making predictions on given data.
            """)

    st.header("Othuke Ajaye- Data Scientist")
    othuke, text3 = st.columns((1,2))
    
    with othuke:
        st.image(othuke_pic)

    with text3:
        st.write("""
            Othuke is a Motivated, teamwork-oriented, and responsible Data Scientist who strives to provide insights to help make informed decisions with skills in 
            data analytics, communication and problem solving.
            """)

    st.header("Joseph Aromeh - Data Scientist")
    joseph, text4 = st.columns((1,2))
    
    with joseph:
        st.image(joseph_pic)

    with text4:
        st.write("""
            A data enthusiast, skilled in Data Visualization with Pandas, Power BI and Machine Learning using Python, PySpark, ScikitLearn, Tensorflow, Serverless Machine Learning.
            """)

    st.header("Ehibhahiemen Ughele - Data Engineer")
    ehi, text5 = st.columns((1,2))
    
    with ehi:
        st.image(ehi_pic)

    with text5:
        st.write("""
            A detail-oriented data engineer highly proficient in the architecture of data oriented infrastructure and solutions to problem utilising skills such as Python, SQL,
             Spark as well as a careful integration of pipelines or cloud related services solutions leveraging on AWS and AZURE.""")

    st.header("Johnson Amodu - Data Scientist")
    johnson, text6 = st.columns((1,2))
    
    with johnson:
        st.image(johnson_pic)

    with text6:
        st.write("""
            A fast learning Data Scientist highly skilled in data wrangling, EDA, and predictive modeling for business operations and development.
            """)

    st.header("David Kambo - Data Scientist")
    david, text7 = st.columns((1,2))
    
    with david:
        st.image(david_pic)

    with text7:
        st.write("""
            A data scientist knowledgeable in data wrangling, data analysis, data visualization and machine learning. Pragmatic and meticulous are adjectives that are often used to describe him.
            """)

    st.header("Theresa Koomson - Data Scientist")
    theresa, text8 = st.columns((1,2))
    
    with theresa:
        st.image(theresa_pic)

    with text8:
        st.write("""
        A motivated data scientist seeking challenging assignments and responsibilities to enhance my professional skill in a dynamic workplace with an opportunity for career advancement and organizational growth as a rewarding achievement
            """)

    st.header("Samson  - Data Scientist")
    samson, text9 = st.columns((1,2))
    
    with samson:
        st.image(samson_pic)

    with text9:
        st.write("""
        A driven data scientist with statistical and predictive analytics skills who can work in a range of data environments. 
        He has the capability to employ programming and research to improve the efficacy and quality of insight extraction.
            """)

    st.header("Hasan A-Raji  - Data Scientist")
    hasan, text10 = st.columns((1,2))
    
    with hasan:
        st.image(hasan_pic)

    with text10:
        st.write("""
        A Data Science prodigy with skills in Pandas, Pyspark, SQL, PowerBI, 
        and Scikitlearn, for Data exploration, analysis, visualisation, and machine learning.
            """)

    
#Landing page
landing = Image.open('Images/waterworksRS (2).png')
if selection == "Home":
    st.image(landing)



#Time Series Page
if selection == 'Time Series':
    ts.main()

#Interactive map page
if selection == 'Water Quality':
    dm.main()
