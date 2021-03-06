# -*- coding: utf-8 -*-
"""hw5

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CP3Tz8oR582rq7E23vU0GxUaMrHQTClL
"""

!pip install spacy
!pip install newsapi-python
!python -m spacy download en_core_web_lg

import newsapi
import spacy
from newsapi import NewsApiClient
import pandas as pd
import pickle
import collections
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from google.colab import files

nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient (api_key='176805c5f7b14d36bcf63be9e846ed21')

def get_keywords_eng(text):
  doc = nlp_eng.tokenizer(text)
  token = doc[0]
  punctuation = ['.','?','!',',',';',':','-',
                 '{','}','[',']','(',')','\'','\"',
                 '...','—']
  pos_tag = ['VERB','NOUN','PROPN']
  result = []
  if (token.text in nlp_eng.Defaults.stop_words or token.text in punctuation): 
    print('a') # continue
  elif (token.pos_ in pos_tag):
    print('b')
    result.append(token.text)
  return result

articles = newsapi.get_everything(q='coronavirus', language='en', 
  from_param='2022-02-27', to='2022-03-26',sort_by='relevancy', page=5)

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))

filename = 'articlesCOVID.pckl'
loaded_model = pickle.load(open(filename, 'rb'))

filepath = 'Downloads'
pickle.dump(loaded_model, open(filepath, 'wb'))

dados = []
titles = []
dates = []
descriptions = []

for i, article in enumerate(articles):
    for x in articles['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title':title, 'date':dates, 
                      'desc':description, 'content':content})
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

#df.to_csv(r'file.csv')
#files.download('file.csv')

results = [] 
for content in df.content.values:
    results.append([('#' + x[0]) for x in 
collections.Counter(get_keywords_eng(content)).most_common(5)])
    
df['keywords'] = results

#text = str(results)
#wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
#plt.show()