# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 21:20:33 2021

@author: fatih
"""

import pymongo


import certifi

import pandas as pd

import numpy as np

import re

from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

import requests



no_pages = 2

global eID

eID = 0

page_url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating"
page_url2 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start=51&ref_=adv_nxt"
uClient = uReq(page_url)
uClient2 = uReq(page_url2)
 

page_soup = soup(uClient.read(), "html.parser")
page_soup2 = soup(uClient2.read(), "html.parser")

#print(page_soup)

uClient.close()
uClient2.close()
 

movies = page_soup.findAll('div', attrs= {'class':'lister-item mode-advanced'})
movies2 = page_soup2.findAll('div', attrs= {'class':'lister-item mode-advanced'})
movies = movies + movies2


#%%

movie_name = []  
year = []
rating = []
duration = []
votes = []
revenue = []
for movie in movies:

    name = movie.h3.a.text

    movie_name.append(name)

   

    year_o_release = movie.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')

    year.append(year_o_release)

   

    rate = movie.find('div', class_='inline-block ratings-imdb-rating'). text.replace('\n', '')

    rating.append(rate)

   

    time = movie.find('span', class_ = 'runtime').text.replace(' min', '')

    duration.append(time)

   

    value = movie.find_all('span', attrs = {'name': 'nv'})

   

    vote = value[0].text

    votes.append(vote)

   

    revenues = value[1].text if len(value) >1 else '**'

    revenue.append(revenues)

results = []


movie_DF = pd.DataFrame({'Movie Name': movie_name, 'Year of Release': year, 'Overall Rating': rating, 'Movie Duration' : duration, 'Collected Votes' : votes, 'Revenues' : revenue   })




print(movie_DF)


#%%

client = pymongo.MongoClient("yourspecialcode")
db=client.database
col = db["col"]


db.col.insert_many(movie_DF.to_dict('records'))
