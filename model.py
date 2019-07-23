#!/usr/bin/env python
# coding: utf-8

# ## model.py

# ##### Accuracy = approx 99%

# ***

# In[66]:


import tensorflow
import pandas
import csv


# In[67]:


#single forward slash for the directory's name because I do not use windows.

import requests
from bs4 import BeautifulSoup
url='https://karki23.github.io/Weather-Data/assignment.html'
a=requests.get(url)
r=BeautifulSoup(a.content, "lxml")
cities=r.find_all('a')
import csv
file_name="dataset/"+"All_Cities."+"csv"
f=open(file_name, "a", newline="")
writer=csv.writer(f)
writer.writerow(['Date','Location','MinTemp','MaxTemp','Rainfall','Evaporation','Sunshine','WindGustDir','WindGustSpeed','WindDir9am','WindDir3pm','WindSpeed9am','WindSpeed3pm','Humidity9am','Humidity3pm','Pressure9am','Pressure3pm','Cloud9am	','Cloud3pm','Temp9am','Temp3pm','RainToday','RISK_MM','RainTomorrow'])
for x in range(len(cities)):
    s=cities[x].get('href')[0:len(cities[x])-5:]    
    new_url='https://karki23.github.io/Weather-Data/'+cities[x].get('href')
    new_a=requests.get(new_url)
    new_r=BeautifulSoup(new_a.content, "lxml")
    row=new_r.find_all('tr')
    row.pop(0) 
    writer=csv.writer(f)
    for i in row:    
        column=i.find_all('td')
        new_column=[j.text for j in column]
        writer.writerow(new_column)
f.close()


# In[68]:


import os
cwd = os.getcwd()
print(cwd)


# In[69]:


os.chdir("/Users/sakshishetty/Desktop/Python/dataset")  #CHANGE ACCORDING TO YOUR SYSTEM
cwd = os.getcwd()
print(cwd)


# In[70]:


dataset = pandas.read_csv('All_Cities.csv')      #File consisting of data of all 49 cities
dataset = dataset.drop(columns =['Date','Location'])


# (read the comments)

# In[71]:


'''from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
dataset['RainToday']=encoder.fit_transform(dataset['RainToday'])
I initially tried using this method for all the string data, but I got an error I wasn't able to fix, 
so I opted for the method below.
'''

dataset['WindGustDir'] = pandas.Categorical(dataset['WindGustDir'])
dataset['WindGustDir'] = dataset.WindGustDir.cat.codes
dataset['WindDir9am'] = pandas.Categorical(dataset['WindDir9am'])
dataset['WindDir9am'] = dataset.WindDir9am.cat.codes
dataset['WindDir3pm'] = pandas.Categorical(dataset['WindDir3pm'])
dataset['WindDir3pm'] = dataset.WindDir3pm.cat.codes
dataset['RainTomorrow'] = pandas.Categorical(dataset['RainTomorrow'])
dataset['RainTomorrow'] = dataset.RainTomorrow.cat.codes
dataset['RainToday'] = pandas.Categorical(dataset['RainToday'])
dataset['RainToday'] = dataset.RainToday.cat.codes

dataset[['WindGustDir','WindDir9am','WindDir3pm']] = dataset[['WindGustDir','WindDir9am','WindDir3pm']].astype(float)

#to get rid of negative values
import numpy as np
dataset[['WindDir9am']] = np.where(dataset[['WindDir9am']]<0, 0, dataset[['WindDir9am']])
dataset[['WindGustDir']] = np.where(dataset[['WindGustDir']]<0, 0, dataset[['WindGustDir']])
dataset[['WindDir3pm']] = np.where(dataset[['WindDir3pm']]<0, 0, dataset[['WindDir3pm']])
dataset[['RainToday']] = np.where(dataset[['RainToday']]<0, 0, dataset[['RainToday']])

#filling the missing values with mean
dataset.fillna(dataset.mean(), inplace=True)


# In[72]:


seed = 42
np.random.seed(seed)


# In[73]:


xtrain = dataset.drop(columns=['RainTomorrow'])
ytrain = dataset['RainTomorrow']


# In[74]:


from keras.models import Sequential
from keras.layers import Dense
model = Sequential()
n = xtrain.shape[1]  #number of columns in training data

model.add(Dense(250, activation='sigmoid', input_shape=(n,)))
model.add(Dense(250, activation='sigmoid'))
model.add(Dense(250, activation='sigmoid'))
model.add(Dense(2, activation='sigmoid'))
#accuracy seems to vary vastly based on the usage of sigmoid or relu or softmax


# In[75]:


model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy',
             metrics = ['accuracy'])


# In[76]:


model.fit(xtrain, ytrain, validation_split=0.2, epochs=10)


# ***
