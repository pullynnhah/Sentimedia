import streamlit as st
st.set_page_config(
            page_title="Sentimedia",
            page_icon="🔍",
            layout="wide")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
# import imageio
import folium
from streamlit_folium import folium_static
import folium.plugins as plugins
# from ipywidgets import interact
from wordcloud import WordCloud, STOPWORDS
import spacy
import scattertext as sct
import streamlit.components.v1 as components
import base64

data_path = 'raw_data/yelp_academic_dataset_business.json'

city_name_input = "Boston"
rest_name_input = "Burger King"
rating_input = 3

#  RESTAURANTS MAP

# cache loaded restaurants from dataset businesses
@st.cache
def get_cached_data():
    df_origin = pd.read_json(data_path, lines=True)
    df_open = df_origin[df_origin['is_open']==1]
    df_restaurants = df_open[df_open.categories.notna()]
    df_restaurants = df_restaurants[df_restaurants.categories.str.contains("Restaurants")]
    df_restaurants = df_restaurants[(df_restaurants.city == 'Boston') | (df_restaurants.city == 'Westerville')]
    return df_restaurants

df = get_cached_data()

# get cordinates of city name
def loc_city(city_name):
  city = df[df['city'] == city_name].sort_values('stars')
  lon = city['longitude'].median()
  lat = city['latitude'].median()
  data=[]
  stars_list=list(city['stars'].unique())
  for star in stars_list:
      subset=city[city['stars']==star]
      data.append(subset[['latitude','longitude','stars']].values.tolist())
  data = [item for sublist in data for item in sublist]
  return data, lon, lat

# get cordinates of a specific restaurant name
def rest_coord(rest_name,city_name):
  rest_data = df[(df.name == rest_name)&(df.city == city_name)][['latitude','longitude']].values.tolist()
  return rest_data

# build map with folium and insert markers on it
def make_folium(city_name,rest_name,rating):
  data, lon, lat = loc_city(city_name)
  rest_data = rest_coord(rest_name,city_name)
  m = folium.Map(location=[lat, lon], tiles="OpenStreetMap", zoom_start=11)
  marker_cluster = folium.plugins.MarkerCluster().add_to(m)
  for point in range(0, len(data)):
    if data[point][:-1] in rest_data:
      folium.Marker(data[point][:-1], icon=folium.Icon(color='red',icon='bar-chart', prefix='fa'), popup=rest_name).add_to(m)
    if data[point][-1] > rating:
      folium.Marker(data[point][:-1],popup=str(data[point][-1])).add_to(marker_cluster)
  return m

map = make_folium(city_name_input, rest_name_input, rating_input)
# display map on streamlit
# map2 = folium_static(map)

# LAYING OUT THE TOP SECTION OF THE APP

ELEMENT_HTML = f"""
<div id="logo">
</div>
"""
st.write(ELEMENT_HTML, unsafe_allow_html=True)

row1_1, row1_2, row1_3 = st.beta_columns((10,1,15))


# text input and slider to interact with map
with row1_1:
  st.markdown("""
  ## Locate restaurants in the map by city and rating""")
  st.write('Displaying map for the city of ', city_name_input.upper())
  city_name_input = st.text_input('City Name', 'Boston')
  rating_input = st.slider('Rating: select the minimum', 0.0 , 5.0 , 0.0, 0.5)
  rest_name_input = st.text_input('Restaurant Name', 'Burger King')
  st.write('Restaurants named ', rest_name_input.upper(), ' are marked with red pins on the map')

  
with row1_2:
  st.markdown("""# """)

with row1_3:
  folium_static(map)

folium_static(map)
folium_static(map)



@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-position: top;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def set_png_as_page_bg2(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    #logo {
    background-image: url("data:image/png;base64,%s");
    height: 115px;
    background-size: contain;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_png_as_page_bg('cinza.png')
###set_png_as_page_bg('gradient faded.png')
# set_png_as_page_bg('gradient.png')
# set_png_as_page_bg('gravura azul.png')
##set_png_as_page_bg('gravura retro.png')
## set_png_as_page_bg('nordico.png')
###set_png_as_page_bg('gravura faded.png')
##set_png_as_page_bg('faded.png')
# set_png_as_page_bg2('logo.png')
set_png_as_page_bg2('logo2.png')

CSS = """
h1 {
  color: black;
  font-size: 60px;
}
h2 {
  color: #F63366;
}
p {
  color: black;
}
"""  
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


# ELEMENT_CSS = f"""
# #elements {{
#   height: 220px;
#   width: 100%;
#   display: flex;
#   align-items: center;
#   justify-content: space-evenly;
# }}
# #element {{
#   height: 200px;
#   width: 200px;
# }} 
# """

# ELEMENT_HTML = f"""
# <style>
# {ELEMENT_CSS}
# </style>
# <div id="elements">
#   <h1>HI THERE</h1>
#   <p>HI THERE</p>
#   {city_name_input}
# </div>
# """

# st.write(ELEMENT_HTML, unsafe_allow_html=True)

# components.html(f"""
# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
# <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
# <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
# <div class="container">
#   <div class="row">
#     <div class="col">{folium_static(map)}</div>
#     <div class="col">{folium_static(map)}</div>
#   </div>
# </div>
# """)