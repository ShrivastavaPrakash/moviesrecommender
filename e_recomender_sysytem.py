# -*- coding: utf-8 -*-
"""e_recomender_sysytem.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YJQZwv9O1pQrBSaIyCjkJIS0Y_HGpNlC
"""

import numpy
import pandas as pd

credits = None



movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')

movies.head(5)

credits.head(5)

credits.head()['cast'].values

#merging two dataset based on title
merged=movies.merge(credits,on='title')

merged.shape

movies.shape

credits.shape

movies=merged

movies.shape

movies.head(1)

movies.info()

# refing the datast that is keeping that is relevent for contebt based recomendation. that is making tags.
#thet are , Genres, id(poster), keywors, title, overview(for content similarity), cast, crew

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head()



from types import prepare_class
#crating new dtaframe form he this dataframe by making tags by adding some of colums to make the tags and data more relivent.
#like adding overview,genres,keywords,cast,crew
#ie. data preprocessing removing null values

movies.isnull().sum()

#drop the null values
movies.dropna(inplace=True)

movies.isnull().sum()

#for duplicate data
movies.duplicated().sum()

#correcting the formate of the data frame

movies.iloc[0]

movies.iloc[0].genres

# now here perform preprocessing to make the data given in the formate
# ['Action','Adventure','Fantasy','Scifi']
#As the list is a srting of list so we must first convert it list
#by creating a helper function to convert this
import ast # for calling the literal eval modudle for conversion of (string of list) to list
def convert(obj):
  L= []#list
  for i in  ast.literal_eval(obj):
    L.append(i['name'])
  return L

movies['genres']=movies['genres'].apply(convert)

movies.head()

#similar we perform on the keywors
movies['keywords']=movies['keywords'].apply(convert)

movies.head()

#similar for cast as we only extract the top casts
movies['cast'][5]

# so here we only want actual name not character name

def convert3(obj):
  L= []
  counter=0
  for i in  ast.literal_eval(obj):
    L.append(i['name'])
    counter+=1
    if counter==3:
      break
  return L

movies['cast']=movies['cast'].apply(convert3)

movies.head()

# for crew  we only tkae director name only so we have to extracvt the job:director dicitnory

def find_dir(obj):
  L= []#list
  for i in  ast.literal_eval(obj):
    if i['job']=='Director':
      L.append(i['name'])
      break
  return L

movies['crew']=movies['crew'].apply(find_dir)

movies.head()

# for overview as it is a string now convert this into a list
movies['overview'][0]

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()



#now apply the transformation on the dataset to make into one tag(token eg johny deep beame jhoneydeep)
#a bcz. it does not get confussed with same first or last names

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

#simaliary for al th eothers like keyword cast and crew

movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

#now we create a tag inside movies in which concentate the other tags like cast crew and keywords and genure.

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

movies.head() #concentated final column

# create a new df to store it

new_df=movies[['movie_id','title','tags']]

new_df.head()

#convert the list into the string

new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))

new_df.head()

new_df['tags'][0] #showing the joined column

new_df['tags']=new_df['tags'].apply(lambda x:x.lower())#for lower case

new_df.head()

#apply steaming to remove silmar words like actions, actions
#bcz these will make rather not effectinve system and not so refined data

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

#helper function

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

# vectorrization of text making tokens and assign them
#as here neede to find simililarity between the two as to give recomendation by making vacteor (bag of words counting frequeny of word)
#and suggesting the nearest vectorized content nearst ot the just watched as we can see below

new_df['tags'][0]

new_df['tags'][1]

#as seen above we have to find similirites
#so perform vectorzition by using libray sciket learn(count vectoriozor)

from sklearn.feature_extraction.text import CountVectorizer

countVec = CountVectorizer(max_features=5000, stop_words='english')

vectors=countVec.fit_transform(new_df['tags']).toarray()

countVec.fit_transform(new_df['tags']).toarray().shape

vectors

vectors[0]

countVec.get_feature_names_out()



countVec.get_feature_names_out()[2000:5000]

countVec.get_feature_names_out()[2000:5000]

ps.stem('hearted')

ps.stem('hearts')

#now calulate cosine distance(not elucidine) as it calculade angle(theta btw them)
#like in clustring
from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(vectors)

cosine_similarity(vectors).shape

similarity=cosine_similarity(vectors)

similarity[0]#WITH ITSELF IS ALWAYS 1

similarity[1]

#now nmake a model function that will give the simliar movie name as inputed a movie name
#by finding the index and the find the distances by sorting

def recommend(movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:       #print(i[0]) will give only index
    print(new_df.iloc[i[0]].title)#so for tilte we will use iloc.title

recommend('Batman Begins')

recommend('Avatar')

recommend('Iron Man')



# now making the website

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))

new_df['title'].values

pickle.dump(similarity,open('similarity.pkl','wb'))

