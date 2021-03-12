import streamlit as st
import Sentimedia.data_viz as dv
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import WordCloud
from streamlit_echarts import st_pyecharts
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import streamlit.components.v1 as components
import base64
import requests
import time


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
            page_title="Sentimedia",
            page_icon="🔍",
            layout="wide")

# import numpy as np
# import pandas as pd

# # import seaborn as sns
# # import imageio
# import folium

# import folium.plugins as plugins
# # from ipywidgets import interact
# from wordcloud import WordCloud, STOPWORDS
# import spacy
# import scattertext as sct
# import spacy_streamlit
# from streamlit_lottie import st_lottie

#DEFAULT PARAMETERS
city_name_input = "Boston"
rest_name_input = "Longwood Galleria"
rating_input = 3

words = ['food', 'place', 'court', 'good', 'lunch', 'mcdonalds', 'cvs', 'get', 'like', 'mall']

#LAYING OUT THE SIDE BAR
st.sidebar.markdown(f"""
  # CONTROL PANEL
  ###
""")

st.sidebar.header('Map Selections')
city_name_input = st.sidebar.text_input('City Name', 'Boston')
rating_input = st.sidebar.slider('Rating: select a minimum', 0.0 , 5.0 , 3.0, 0.5)
rest_name_input = st.sidebar.text_input('Restaurant Name', 'Longwood Galleria', key='rest_name_input')

st.sidebar.markdown(f"""
  #
""")
st.sidebar.header('Word Cloud and Bar Chart Selections')
double_entry = st.sidebar.radio('Benchmark your business to others', ('Single View', 'Display Benchmark'))
st.sidebar.write(double_entry)
# double_entry = st.sidebar.checkbox('Benchmark your business to others')

rest_name_input2 = 'Longwood Galleria'
rest_name_input2 = st.sidebar.text_input('Restaurant Name', 'Longwood Galleria', key='rest_name_input2')
if double_entry == 'Display Benchmark':
  st.sidebar.subheader('Select a business for Benchmarking')
  rest_name_input3 = 'Longwood Galleria'
  rest_name_input3 = st.sidebar.text_input('Comparative Restaurant Name', 'Longwood Galleria', key='rest_name_input3')

#STOP WORDS SELECTIONS
st.sidebar.subheader("Improve visualizations by excluding potential stop words")
st.sidebar.text('Pick stop words below, if any')
for word in words:
  word = st.sidebar.checkbox(word)

# LAYING OUT THE TOP SECTION OF THE APP

ELEMENT_HTML = f"""
<div id="logo">
</div>
"""
st.write(ELEMENT_HTML, unsafe_allow_html=True)

row1_1, row1_2, row1_3 = st.beta_columns((10,1,15))
with row1_1:
  st.markdown("""
  ## Locate restaurants in the map by city and rating""")


with row1_2:
  st.markdown("""# """)

with row1_3:
  map = dv.make_folium(city_name_input, rest_name_input, rating_input)
  st.write('Displaying the city of ', city_name_input.upper(), '. Restaurants named ', rest_name_input.upper(), ' are the red pins')
  folium_static(map)

st.markdown("""# """)

if double_entry == 'Display Benchmark':
  col1, col2, col3 = st.beta_columns((12,1,12))
  with col1:
    HEADER_HTML = f"""
      <div><h2>Word Cloud for negative and positive reviews</h2>
      </div>
    """
    st.write(HEADER_HTML, unsafe_allow_html=True)
    wordcloud = dv.make_wordcloud(rest_name_input2)
    plt.show()
    st.pyplot(wordcloud)
    st.markdown("""# """)
    HEADER_HTML3 = f"""
      <div><h2>Word Cloud for comparative business </h2>
      </div>
    """
    st.write(HEADER_HTML3, unsafe_allow_html=True)
    wordcloud = dv.make_wordcloud(rest_name_input3)
    plt.show()
    st.pyplot(wordcloud)

  with col2:
    st.markdown("""# """)

  with col3:
    HEADER_HTML2 = f"""
      <div><h2>Bar Chart for negative and positive reviews</h2>
      </div>
    """
    st.write(HEADER_HTML2, unsafe_allow_html=True)
    barplot = dv.make_barplot(rest_name_input2)
    plt.show()
    st.pyplot(barplot)
    HEADER_HTML4 = f"""
      <div><h2>Word Cloud for comparative business</h2>
      </div>
    """
    st.write(HEADER_HTML4, unsafe_allow_html=True)
    barplot = dv.make_barplot(rest_name_input3)
    plt.show()
    st.pyplot(barplot)
else:
  HEADER_HTML = f"""
    <div><h2>Word Cloud for negative and positive reviews</h2>
    </div>
  """
  st.write(HEADER_HTML, unsafe_allow_html=True)
  wordcloud = dv.make_wordcloud(rest_name_input2)
  plt.show()
  st.pyplot(wordcloud)
  HEADER_HTML2 = f"""
    <div><h2>Bar Chart for negative and positive reviews</h2>
    </div>
  """
  st.write(HEADER_HTML2, unsafe_allow_html=True)
  barplot = dv.make_barplot(rest_name_input2)
  plt.show()
  st.pyplot(barplot)

# b = (
#     Bar()
#     .add_xaxis(['food', 'place', 'court', 'good', 'lunch', 'mcdonalds', 'cvs', 'get', 'like', 'mall'])
#     .add_yaxis(
#         "Frequecy of most frequent words in negative reviews", [27, 24, 15, 12, 12, 11, 10, 10, 9, 9]
#     )
#     .set_global_opts(
#         title_opts=opts.TitleOpts(
#             title="Top words from negative reviews", subtitle="Frequency"
#         ),
#         toolbox_opts=opts.ToolboxOpts(),
#     )
# )
# st_pyecharts(b)

# data = [
#     ("food", "27"),
#     ("place", "24"),
#     ("court", "15"),
#     ("good", "12"),
#     ("lunch", "12"),
#     ("mcdonalds", "11"),
#     ("cvs", "10"),
#     ("get", "10"),
#     ("like", "9"),
#     ("mall", "9"),
#     ("ive", "8"),
#     ("places", "7"),
#     ("would", "7"),
#     ("burrito", "7"),
#     ("parking", "7"),
#     ("area", "7"),
#     ("work", "6"),
#     ("chinese", "6"),
#     ("pretty", "6"),
#     ("really", "6"),
#     ("every", "6"),
#     ("part", "6"),
#     ("subway", "6"),
#     ("go", "6"),
#     ("one", "6"),
#     ("options", "5"),
#     ("galleria", "5"),
#     ("never", "5"),
#     ("people", "5"),
#     ("decent", "5"),
# ]

# c = (
#     WordCloud()
#     .add(series_name="frequent words", data_pair=data, word_size_range=[6, 66])
#     .set_global_opts(
#         title_opts=opts.TitleOpts(
#             title="Wordcloud", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
#         ),
#         tooltip_opts=opts.TooltipOpts(is_show=True),
#     )
# )
# st_pyecharts(c)





# SCATTER_HTML = dv.get_sct_html('Longwood Galleria', 'Boston')
# spacy_streamlit.visualize(SCATTER_HTML)
# st.write({SCATTER_HTML}, unsafe_allow_html=True)

# html = dv.get_sct_html('Longwood Galleria', 'Boston')
# components.html(f"""
#   {html}
#   """,
#   height=600,
# )




#STYLING CODE

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

# set_png_as_page_bg('cinza.png')
set_png_as_page_bg('gradient faded.png')
# set_png_as_page_bg('gradient.png')
# set_png_as_page_bg('gravura azul.png')
# set_png_as_page_bg('gravura retro.png')
# set_png_as_page_bg('nordico.png')
# set_png_as_page_bg('gravura faded.png')
# set_png_as_page_bg('faded.png')
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