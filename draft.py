# WORDS CLOUD
review_json_path = '../raw_data/yelp_academic_dataset_review.json'

@st.cache(allow_output_mutation=True)
def get_cached_data2():
  size = 1000
  df_reviews = pd.read_json(review_json_path, lines=True,
                        dtype={'review_id':str,'user_id':str,
                              'business_id':str,'stars':int,
                              'date':str,'text':str,'useful':int,
                              'funny':int,'cool':int},
                        chunksize=size)
  return df_reviews

review = get_cached_data2()
df_100 = df.sort_values('review_count', ascending=False).head(100)

chunk_list = []
for chunk_review in review:
    chunk_review = chunk_review.rename(columns={'stars': 'review_stars'})
    chunk_merged = pd.merge(df_100, chunk_review, on='business_id', how='inner')
    # print(f"{chunk_merged.shape[0]} out of {size:,} related reviews")
    chunk_list.append(chunk_merged)

# After trimming down the review file, concatenate all relevant data back to one dataframe
df_sample = pd.concat(chunk_list, ignore_index=True, join='outer', axis=0)

def clean_text(s):
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = s.lower()
    return s.split()

df_1 = df_sample[df_sample['business_id']=='4CxF8c3MB7VAdY8zFb2cZQ']
text_1 = [clean_text(x) for x in df_1.text]
text_1 = [item for sublist in text_1 for item in sublist]

stopwords = set(STOPWORDS)
stopwords.update(["donut","donuts" ,"doughnut","doughnuts","Voodoo", "Portland"])

wordcloud = WordCloud(stopwords=stopwords).generate(' '.join(df_1.text))

# Display the generated image:
plt.figure(figsize=(15,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

st.write(plt.show())


# SCATTERTEXT

review_json_path = '../raw_data/yelp_academic_dataset_review.json'
df_sample = pd.read_json(review_json_path, lines=True,
                        dtype={'review_id':str,'user_id':str,
                              'business_id':str,'stars':int,
                              'date':str,'text':str,'useful':int,
                              'funny':int,'cool':int},
                        nrows=1000)

nlp = spacy.load('en_core_web_sm')

def good_bad_review(x):
  if x >= 4:
      return 'good'
  return 'bad'

def get_rest_reviews(rest_name, city_name):
  rest_reviews = df_sample[(df_sample.name == rest_name)&(df_sample.city == city_name)][['name','city','stars','review_stars','text']]
  rest_reviews['class'] = rest_reviews.review_stars.map(good_bad_review)
  return rest_reviews

def get_sct_html(rest_name, city_name):
  rest_reviews = get_rest_reviews(rest_name, city_name)
  corpus = sct.CorpusFromPandas(rest_reviews,
                            category_col='class',
                            text_col='text',
                            nlp=nlp).build()
  html = sct.produce_scattertext_explorer(corpus,
        category='good',
        category_name='Positive',
        not_category_name='Negative',
        width_in_pixels=1000,
        metadata=rest_reviews['class'])
  return open("rest_reviews-Vis.html", 'wb').write(html.encode('utf-8'))