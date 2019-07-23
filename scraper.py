import requests
from bs4 import BeautifulSoup
url='https://karki23.github.io/Weather-Data/assignment.html'
a=requests.get(url)
r=BeautifulSoup(a.content, "lxml")
cities=r.find_all('a')
import csv
import os
os.mkdir("dataset/")
for x in cities:
    s=x.get('href')[0:len(x)-5:]    
    new_url='https://karki23.github.io/Weather-Data/'+x.get('href')
    new_a=requests.get(new_url)
    new_r=BeautifulSoup(new_a.content, "lxml")
    row=new_r.find_all('tr')
    row.pop(0) 
    fnames="dataset/"+s+"csv"  
    f=open(fnames, "w", newline="")
    writer=csv.writer(f)
    writer.writerow(['Date','Location','MinTemp','MaxTemp','Rainfall','Evaporation','Sunshine','WindGustDir','WindGustSpeed','WindDir9am','WindDir3pm','WindSpeed9am','WindSpeed3pm','Humidity9am','Humidity3pm','Pressure9am','Pressure3pm','Cloud9am	','Cloud3pm','Temp9am','Temp3pm','RainToday','RISK_MM','RainTomorrow'])
    for i in row:    
        column=i.find_all('td')
        new_column=[j.text for j in column]
        writer.writerow(new_column)
    f.close()