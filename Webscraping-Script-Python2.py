
# WEBSCRAPING AND BEYOND
#
# Blog including code: https://www.rrighart.com/blog-webscraping/webscraping-and-beyond
# Ruthger Righart
# 
# Email: rrighart@googlemail.com
# Website: www.rrighart.com

import warnings
warnings.filterwarnings("ignore")

# Healthcare rankings for different European countries 

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import re
import urllib2
from datetime import datetime
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

os.chdir('/your-directory/')os.getcwd()

url = 'https://en.wikipedia.org/wiki/Healthcare_in_Europe' 
r = requests.get(url)
HCE = BeautifulSoup(r.content)
type(HCE)

htmlpage = urllib2.urlopen(url)
lst = []
for line in htmlpage:
    line = line.rstrip()
    if re.search('table class', line) :
        lst.append(line)

len(lst)
lst

table=HCE.find('table', {'class', 'wikitable sortable'})

x=lst[0]
extr=re.findall('"([^"]*)"', x)
table=HCE.find('table', {'class', str(extr).strip("'[]'")})
type(table)

headers= [header.text for header in table.find_all('th')]
headers

rows = []
for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')])

df1 = pd.DataFrame(rows, columns=headers)

df1.head(7)

# Health Expenditure

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_total_health_expenditure_per_capita' 
r = requests.get(url)
HEE = BeautifulSoup(r.content)
htmlpage = urllib2.urlopen(url)
lst = []

for line in htmlpage:
    line = line.rstrip()
    if re.search('table class', line) :
        lst.append(line)
x=lst[1]
print x
extr=re.findall('"([^"]*)"', x)
table=HEE.find('table', {'class', 'wikitable sortable'})
headers= [header.text for header in table.find_all('th')]
rows = []

for row in table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')])
headers = [i.replace("\n", "") for i in headers]
df2 = pd.DataFrame(rows, columns=headers)

df2.head()

# Additional preprocessing steps

def preproc(dat):
    dat.dropna(axis=0, how='all', inplace=True)
    dat.columns = dat.columns.str.replace("\n", "")    
    dat.replace(["\n"], [""], regex=True, inplace=True)
    dat.replace([","], [""], regex=True, inplace=True)
    dat.replace(r"\b[a-zA-Z]\b", np.nan, regex=True, inplace=True)
    dat = dat.apply(pd.to_numeric, errors='ignore')    
    return(dat)

df1 = preproc(df1)
df2 = preproc(df2)

print(df1.isnull().sum().sum())
print(df2.isnull().sum().sum())

df1[df1.isnull().any(axis=1)]

df1.dropna(axis=0, how='any', inplace=True)

df1.dtypes
df2.dtypes

df1.columns = ['Country', 'Ranking', 'totalscore', 'Patientrights', 'Accessibility', 'Outcomes', 'Range', 'Prevention', 'Pharmaceuticals']
df2.columns = ['Country', 'y2013', 'y2014', 'y2015', 'y2016']

# Merging different data

pd.merge(df1, df2, how='left', on='Country').head()

set(df1['Country']) & set(df2['Country'])

df1.to_csv('df1example.csv', sep=",")
df2.to_csv('df2example.csv', sep=",")

repr(df1['Country'])
repr(df2['Country'])

df1.replace(["\n"],[""], regex=True, inplace=True)
df1.replace(["\xc2\xa0"], [""], regex=True, inplace=True)

set(df1['Country']) & set(df2['Country'])

df3 = pd.merge(df1,df2, how='left', on='Country')
df3.dropna(how='any', inplace=True)

# Data visualization

reload(sys)
sys.setdefaultencoding('utf8')

df3['Avg'] = df3.loc[:, ['y2013', 'y2014', 'y2015', 'y2016'] ].mean(axis=1)

xmin=df3.Patientrights.min()-10
xmax=df3.Patientrights.max()+10
ymin=df3.Outcomes.min()-10
ymax=df3.Outcomes.max()+10

import matplotlib as mpl
import matplotlib.pyplot as plt
from adjustText import adjust_text

def plot_df3(adjust=True):
    mpl.rcParams['font.size'] = 12.0
    plt.figure(figsize = (14, 14))
    plt.scatter(df3.Patientrights, df3.Outcomes, facecolors='none', edgecolors='red', linewidth=1.2, s=1*df3.Avg)
    texts = []
    plt.title('Relation between different health parameters')
    plt.xlabel('Patient rights')
    plt.ylabel('Outcomes')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    for x, y, s in zip(df3['Patientrights'], df3['Outcomes'], df3['Country']):
        texts.append(plt.text(x, y, s, size=12))
    if adjust:
        plt.title(str(adjust_text(texts, arrowprops=dict(arrowstyle="-", color='black', lw=0.5))
))

_ = plot_df3()
plt.show()

# Any questions or comments? 
# 
# Please feel free to contact me : 
# 
# Ruthger Righart
# 
# E: rrighart@googlemail.com
# W: https://www.rrighart.com
# 
# (c) 2018 . https://www.rrighart.com | https://rrighart.github.io
