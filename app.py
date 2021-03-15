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

rest_name_input2 = 'Longwood Galleria'
rest_name_input3 = 'Burger King'
rest_name_input2 = st.sidebar.text_input('Business Name', 'Longwood Galleria', key='rest_name_input2')
if double_entry == 'Display Benchmark':
  st.sidebar.subheader('Select a business for Benchmarking')
  rest_name_input3 = st.sidebar.text_input('Benchmark Business Name', 'Burger King', key='rest_name_input3')


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
c_positive_bench, c_negative_bench, data_positive_bench, data_negative_bench = dv.make_wordcloud_interactive(rest_name_input3, [], [])
b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, [], [])
b_pos_bench, b_neg_bench = dv.make_barplot_interactive(rest_name_input3, [], [])


if double_entry == 'Display Benchmark':
  HEADER_HTML = f"""
  <div><h1>GET INSIGHTFUL VISUAL INFORMATION</h1>
  </div>
  """
  st.write(HEADER_HTML, unsafe_allow_html=True)
  st.subheader("Improve visualizations by excluding stop words")
  st.text('select stop words below for POSITIVE reviews')
#DOUBLE VIEW POSITIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_pos_one = make_checkbox_one(data_positive)
  with col2:
    st.markdown("""# """)
    checkboxes_pos_two = make_checkbox_two(data_positive)
  with col3:
    st.markdown("""# """)
    checkboxes_pos_three = make_checkbox_three(data_positive)
    st.markdown("""# """)
    words_list_pos = [x[0] for x in data_positive]
    checked_pos_words = [word for word, checked in zip(words_list_pos, checkboxes_pos_one + checkboxes_pos_two + checkboxes_pos_three) if checked]
    if st.button("Remove stop words", key="positive"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, checked_pos_words, [])
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, checked_pos_words, [])
  with col4:
    st.markdown("""## """) 
  with col5:
    st_pyecharts(c_positive,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20",
      },
    )
    st_pyecharts(
      b_pos,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
          "subtitle_textstyle_opts": {"color": "#F63366"},
      },
    )
  st.text('BENCHMARK: select stop words below for POSITIVE reviews')
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_pos_one_bench = make_checkbox_one(data_positive_bench)
  with col2:
    st.markdown("""# """)
    checkboxes_pos_two_bench = make_checkbox_two(data_positive_bench)
  with col3:
    st.markdown("""# """)
    checkboxes_pos_three_bench = make_checkbox_three(data_positive_bench)
    st.markdown("""# """)
    words_list_pos_bench = [x[0] for x in data_positive_bench]
    checked_pos_words_bench = [word for word, checked in zip(words_list_pos_bench, checkboxes_pos_one_bench + checkboxes_pos_two_bench + checkboxes_pos_three_bench) if checked]
    if st.button("Remove stop words", key="positive_bench"):
      c_positive_bench, c_negative_bench, data_positive_bench, data_negative_bench = dv.make_wordcloud_interactive(rest_name_input3, checked_pos_words_bench, [])
      b_pos_bench, b_neg_bench = dv.make_barplot_interactive(rest_name_input3, checked_pos_words, [])
  with col4:
    st.markdown("""## """)
  with col5:
    st_pyecharts(c_positive_bench,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20",
      },
    )
    st_pyecharts(
      b_pos_bench,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
      },
    )
  st.text('select stop words below for NEGATIVE reviews')
#DOUBLE VIEW NEGATIIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_neg_one = make_checkbox_one(data_negative)
  with col2:
    st.markdown("""# """)
    checkboxes_neg_two = make_checkbox_two(data_negative)
  with col3:
    st.markdown("""# """)
    checkboxes_neg_three = make_checkbox_three(data_negative)
    st.markdown("""# """)
    words_list_neg = [x[0] for x in data_negative]
    checked_neg_words = [word for word, checked in zip(words_list_neg, checkboxes_neg_one + checkboxes_neg_two + checkboxes_neg_three) if checked]
    if st.button("Remove stop words", key="negative"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, [], checked_neg_words)
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, [], checked_neg_words)
  with col4:
    st.markdown("""## """) 
  with col5:
    st_pyecharts(c_negative,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20",
      },
    )
    st_pyecharts(
      b_neg,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
          "subtitle_textstyle_opts": {"color": "#F63366"},
      },
    )
  st.text('BENCHMARK: select stop words below for NEGATIVE reviews')
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_neg_one_bench = make_checkbox_one(data_negative_bench)
  with col2:
    st.markdown("""# """)
    checkboxes_neg_two_bench = make_checkbox_two(data_negative_bench)
  with col3:
    st.markdown("""# """)
    checkboxes_neg_three_bench = make_checkbox_three(data_negative_bench)
    st.markdown("""# """)
    words_list_neg_bench = [x[0] for x in data_negative_bench]
    checked_neg_words_bench = [word for word, checked in zip(words_list_neg_bench, checkboxes_neg_one_bench + checkboxes_neg_two_bench + checkboxes_neg_three_bench) if checked]
    if st.button("Remove stop words", key="negative_bench"):
      c_positive_bench, c_negative_bench, data_positive_bench, data_negative_bench = dv.make_wordcloud_interactive(rest_name_input3, [], checked_neg_words_bench)
      b_pos_bench, b_neg_bench = dv.make_barplot_interactive(rest_name_input3, [], checked_neg_words)
  with col4:
    st.markdown("""## """)
  with col5:
    st_pyecharts(c_negative_bench,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20",
      },
    )
    st_pyecharts(
      b_neg_bench,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
      },
    )

else:
  HEADER_HTML = f"""
    <div><h1>GET INSIGHTFUL VISUAL INFORMATION</h1>
    </div>
  """
  st.write(HEADER_HTML, unsafe_allow_html=True)
  st.subheader("Improve visualizations by excluding stop words")
  st.text('select stop words below for POSITIVE reviews')
#SINGLE VIEW POSITIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  checked_pos_words = []
  checked_neg_words = []
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_pos_one = make_checkbox_one(data_positive)
  with col2:
    st.markdown("""# """)
    checkboxes_pos_two = make_checkbox_two(data_positive)
  with col3:
    st.markdown("""# """)
    checkboxes_pos_three = make_checkbox_three(data_positive)
    st.markdown("""# """)
    words_list_pos = [x[0] for x in data_positive]
    checked_pos_words = [word for word, checked in zip(words_list_pos, checkboxes_pos_one + checkboxes_pos_two + checkboxes_pos_three) if checked]
    if st.button("Remove stop words", key="positive"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, checked_pos_words, [])
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, checked_pos_words, checked_neg_words)
  with col4:
    st.markdown("""## """)
  with col5:
    st_pyecharts(c_positive,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20",
      },
    )
    st_pyecharts(
      b_pos,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
      },
    )
  st.markdown("""## """)
 
#SINGLE VIEW NEGATIVE REVIEWS VISUALIZATIONS AND STOPWORDS
  st.text('select stop words below for NEGATIVE reviews')
  col1, col2, col3, col4, col5 = st.beta_columns((2,2,2,1,14))
  with col1:
    st.markdown("""# """)
    checkboxes_neg_one = make_checkbox_one(data_negative)
  with col2:
    st.markdown("""# """)
    checkboxes_neg_two = make_checkbox_two(data_negative)
  with col3:
    st.markdown("""# """)
    checkboxes_neg_three = make_checkbox_three(data_negative)
    st.markdown("""# """)
    words_list_neg = [x[0] for x in data_negative]
    checked_neg_words = [word for word, checked in zip(words_list_neg, checkboxes_neg_one + checkboxes_neg_two + checkboxes_neg_three) if checked]
    if st.button("Remove stop words", key="negative"):
      c_positive, c_negative, data_positive, data_negative = dv.make_wordcloud_interactive(rest_name_input2, checked_pos_words, checked_neg_words)
      b_pos, b_neg = dv.make_barplot_interactive(rest_name_input2, checked_pos_words, checked_neg_words)
      st.write(checked_pos_words)
  with col4:
    st.markdown("""## """)
  with col5:
    st_pyecharts(c_negative,
      theme={
        "width": "1000",
        "height": "800",
        "subtitle_text_size": "20px",
      },
    )
    st_pyecharts(
      b_neg,
      theme={
          "backgroundColor": "#f4cccc",
          "textStyle": {"color": "#F63366"},
          "yaxis_name_pos" : "end",
      },
    )

    
st.markdown("""# """)
HEADER_HTML_BOTTOM = f"""
  <div><h1>WORD FREQUENCY ACROSS CATEGORIES</h1>
  </div>
  """
st.write(HEADER_HTML_BOTTOM, unsafe_allow_html=True)
st.subheader("Find mentions for each word by selecting on the chart or through the search")
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

set_png_as_page_bg('gradient faded.png')
set_png_as_page_bg2('logo2.png')

CSS = """
h1 {
  color: #F63366;
  font-size: 35px;
}
h2 {
  color: #F63366;
}
p {
  color: black;
}
"""  
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
