import streamlit as st
import Sentimedia.data_viz as dv

# import spacy_streamlit
# from streamlit_lottie import st_lottie
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


#DEFAULT PARAMETERS
city_name_input = "Boston"
rest_name_input = "Mike's Pastry"
rating_input = 3

#LAYING OUT THE SIDE BAR
st.sidebar.markdown(f"""
  # CONTROL PANEL
""")

st.sidebar.header('Map Selections')
city_name_input = st.sidebar.text_input('City Name', 'Boston')
rating_input = st.sidebar.slider('Rating: select a minimum', 0.0 , 5.0 , 3.0, 0.5)
rest_name_input = st.sidebar.text_input('Business Name', 'Longwood Galleria', key='rest_name_input')

st.sidebar.markdown(f"""
  #
""")
st.sidebar.header('Word Cloud and Bar Chart Selections')
double_entry = st.sidebar.radio('Benchmark your business to others', ('Single View', 'Display Benchmark'))
# double_entry = st.sidebar.checkbox('Benchmark your business to others')

rest_name_input2 = 'Longwood Galleria'
rest_name_input2 = st.sidebar.text_input('Business Name', 'Longwood Galleria', key='rest_name_input2')
if double_entry == 'Display Benchmark':
  st.sidebar.subheader('Select a business for Benchmarking')
  rest_name_input3 = 'Longwood Galleria'
  rest_name_input3 = st.sidebar.text_input('Benchmark Business Name', 'Longwood Galleria', key='rest_name_input3')


# LAYING OUT THE TOP SECTION OF THE APP

ELEMENT_HTML = f"""
<div id="logo">
</div>
"""
st.write(ELEMENT_HTML, unsafe_allow_html=True)

row1_1, row1_2, row1_3 = st.beta_columns((8,2,13))
with row1_1:
  st.markdown("""
  ## Locate businesses in the map by city and rating""")


with row1_2:
  st.markdown("""# """)

with row1_3:
  map = dv.make_folium(city_name_input, rest_name_input, rating_input)
  st.write('Displaying the city of ', city_name_input.upper(), '. Businesses named ', rest_name_input.upper(), ' are the red pins')
  folium_static(map)

st.markdown("""# """)

#STOP WORDS SELECTIONS

# def make_checkbox(words):
  # words_list = [x[0] for x in words]
  # checkbox1 = []
  # for word in words_list[:15]:
  #   checkbox1.append(st.checkbox(word, key=f'{word}{words}'))
  # checkbox2 = []
  # for word in words_list[15:]:
  #   checkbox2.append(st.checkbox(word, key=f'{word}{words}'))
  # return checkbox1, checkbox2
  
def make_checkbox_one(words):
  words_list = [x[0] for x in words[:10]]
  checkbox = []
  for word in words_list:
      checkbox.append(st.checkbox(word, key=f'{word}{words}'))
  return checkbox

def make_checkbox_two(words):
  words_list = [x[0] for x in words[10:20]]
  checkbox = []
  for word in words_list:
      checkbox.append(st.checkbox(word, key=f'{word}{words}'))
  return checkbox

def make_checkbox_three(words):
  words_list = [x[0] for x in words[20:]]
  checkbox = []
  for word in words_list:
      checkbox.append(st.checkbox(word, key=f'{word}{words}'))
  return checkbox

#VISUALIZATIONS

c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, [], [])
# c_positive_bench, c_negative_bench, data_positive_bench, data_negative_bench = dv.make_wordcloud_interactive(rest_name_input3, [], [])
b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, [], [])



if double_entry == 'Display Benchmark':
  col1, col2, col3 = st.beta_columns((5,10,12))
  with col1:
    HEADER_HTML = f"""
      <div><h2>Word Cloud for negative and positive reviews</h2>
      </div>
    """
    st.write(HEADER_HTML, unsafe_allow_html=True)
    st.sidebar.subheader("Improve visualizations by excluding potential stop words")
    st.sidebar.text('Pick stop words below for positive reviews')
    checkboxes_pos_one = make_checkbox_one(data_positive)
    st.markdown("""# """)
    checkboxes_pos_two = make_checkbox_two(data_positive)
    st.markdown("""# """)
    checkboxes_pos_three = make_checkbox_three(data_positive)
    words_list_pos = [x[0] for x in data_positive]
    checked_pos_words = [word for word, checked in zip(words_list_pos, checkboxes_pos_one + checkboxes_pos_two + checkboxes_pos_three) if checked]
    st.write(checked_pos_words)
    if st.button("Remove positive stop words"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, checked_pos_words, [])
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, checked_pos_words, [])
    # st_pyecharts(c_positive)


    # st.markdown("""# """)
    # # make_checkbox(data_positive)
    # st_pyecharts(c_negative)
    # st.sidebar.subheader("Improve visualizations by excluding potential stop words")
    # st.sidebar.text('Pick stop words below for negative reviews')
    # # make_checkbox(data_negative)
    # st.markdown("""# """)
    # HEADER_HTML3 = f"""
    #   <div><h2>Word Cloud for comparative business </h2>
    #   </div>
    # """
    # st.write(HEADER_HTML3, unsafe_allow_html=True)
    # c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input3, [], [])
    # st_pyecharts(c_positive)
    # st_pyecharts(c_negative)

  with col2:
    # st.markdown("""# """)
    st_pyecharts(c_positive,
      theme={
        "width": "800",
        "height": "500",
      },
    )

  with col3:
    HEADER_HTML2 = f"""
      <div><h2>Bar Chart for negative and positive reviews</h2>
      </div>
    """
    st.write(HEADER_HTML2, unsafe_allow_html=True)

    st_pyecharts(
      b_pos,
      theme={
          # "width": "600",
          # "height": "330",
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
      },
    )


    # barplot = dv.make_barplot(rest_name_input2)
    # plt.show()
    # st.pyplot(barplot)
    # HEADER_HTML4 = f"""
    #   <div><h2>Word Cloud for comparative business</h2>
    #   </div>
    # """
    # st.write(HEADER_HTML4, unsafe_allow_html=True)
    # barplot = dv.make_barplot(rest_name_input3)
    # plt.show()
    # st.pyplot(barplot)
else:
  # HEADER_HTML = f"""
  #   <div><h2>Word Cloud for negative and positive reviews</h2>
  #   </div>
  # """
  # st.write(HEADER_HTML, unsafe_allow_html=True)
  st.subheader("Improve visualizations by excluding potential stop words")
  st.text('Pick stop words below for positive reviews')
#SINGLE VIEW POSITIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  col1, col2, col3, col4, col5, col6 = st.beta_columns((2,2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_pos_one = make_checkbox_one(data_positive)
  with col2:
    st.markdown("""# """)
    checkboxes_pos_two = make_checkbox_two(data_positive)
  with col3:
    st.markdown("""# """)
    checkboxes_pos_three = make_checkbox_three(data_positive)
  with col4:
    st.markdown("""# """)
    words_list_pos = [x[0] for x in data_positive]
    checked_pos_words = [word for word, checked in zip(words_list_pos, checkboxes_pos_one + checkboxes_pos_two + checkboxes_pos_three) if checked]
    if st.button("Remove stop words POSITIVE"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, checked_pos_words, [])
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, checked_pos_words, [])
  with col5:
    st.markdown("""## """)
  with col6:
    st_pyecharts(c_positive,
      theme={
        "width": "1000",
        "height": "800",
      },
    )
    st_pyecharts(
      b_pos,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
      },
    )
  st.markdown("""## """)
#SINGLE VIEW NEGATIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  col1, col2, col3, col4, col5, col6 = st.beta_columns((2,2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_neg_one = make_checkbox_one(data_negative)
  with col2:
    st.markdown("""# """)
    checkboxes_neg_two = make_checkbox_two(data_negative)
  with col3:
    st.markdown("""# """)
    checkboxes_neg_three = make_checkbox_three(data_negative)
  with col4:
    st.markdown("""# """)
    words_list_neg = [x[0] for x in data_negative]
    checked_neg_words = [word for word, checked in zip(words_list_neg, checkboxes_neg_one + checkboxes_neg_two + checkboxes_neg_three) if checked]
    if st.button("Removestop words NEGATIVE"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, [], checked_neg_words)
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, [], checked_pos_words)
  with col5:
    st.markdown("""## """)
  with col6:
    st_pyecharts(c_negative,
      theme={
        "width": "1000",
        "height": "800",
      },
    )
    st_pyecharts(
      b_neg,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
      },
    )

    
st.markdown("""# """)
html = dv.get_sct_html(rest_name_input2, city_name_input)

HtmlFile = open("rest_reviews-Vis.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 10000)


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