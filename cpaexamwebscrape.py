'''
The purpose of this program is to scrape information from the NASBA.org website 
to create a central repository of exam and licensure requirements.


Ryan McBride (2024)
'''

from bs4 import BeautifulSoup 
from urllib.request import urlopen
import pprint
import pandas as pd
import requests
import xlsxwriter
import re
 
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# OPEN THE FILE
#URL = "https://nasba.org/exams/cpaexam/index.php"
#nasba_States = requests.get(URL, headers=HEADERS)

nasba_States = open("./nasba_webscrape/savedpage.html", 'r')

# MAKE A VARIABLE TO CONTAIN ALL OF THE CONTENTS
contents = nasba_States.read()#.text

# MAKE IT BEAUTIFUL USING THE LIBRARY ABOVE
beautifulContents = BeautifulSoup(contents, "lxml")

# PARSE HTML Content
html = beautifulContents.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#pprint.pprint(soup)

savedpage = open("savedpage.html",'w')
savedpage.write(str(soup))
savedpage.close()

# FIND THE TABLE WITH THE STATE LINKS
state_table = soup.find("figure", class_="wp-block-table")
state_table_rows = state_table.find_all("a")
state_links = []
for link in state_table_rows: 
    state_links.append(link.get('href'))


# CONVERT TO DATAFRAME
state_links_df = pd.DataFrame(state_links)
state_links_df.rename({0:'HREF'}, axis=1, inplace=True)


# ADD THE WEB PREFIX
state_links_df['HREF'] = 'https://nasba.org' + state_links_df['HREF'].astype(str)
state_links_df['State'] = state_links_df['HREF'].str.split('/').str[-1]
state_links_df['HREF'] = state_links_df['HREF'].astype(str) + '/index.php'
state_links_df['State'][10] = 'florida' #fix florida being truncated
pprint.pprint(state_links_df)

# GRAB ALL WEB FILES
'''all_page_contents_list = []
for link in range(len(state_links_df)):
    URL = state_links_df['HREF'][link]
    nasba_States = requests.get(URL, headers=HEADERS)
    # MAKE A VARIABLE TO CONTAIN ALL OF THE CONTENTS
    page_contents = nasba_States.text

    # MAKE IT BEAUTIFUL USING THE LIBRARY ABOVE
    beautifulContents = BeautifulSoup(page_contents, "lxml")

    # PARSE HTML Content
    html = beautifulContents.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    all_page_contents_list.append(str(soup))

all_page_contents_list_df = pd.DataFrame(all_page_contents_list)
all_page_contents_list_df.to_csv('all_page_contents_list.csv', index=False)
pprint.pprint(all_page_contents_list)

# GRAB ALL OF THE WEB FILES FROM LIST EXPORTED ABOVE
'''
saved_export = pd.read_csv('nasba_webscrape/all_page_contents_list.csv')
saved_export.rename({'0': 'HTML'}, axis=1, inplace=True)
#pprint.pprint(saved_export)

alabama, alaska, arizona, arkansas, california, cnmi, colorado, connecticut, delaware, dc, florida, georgia, guam, hawaii, idaho, illinois, indiana, iowa, kansas, kentucky, louisiana, maine, maryland, massachusetts, michigan, minnesota, mississippi, missouri, montana, nebraska, nevada, newhampshire, newjersey, newmexico, newyork, northcarolina, northdakota, ohio, oklahoma, oregon, pennsylvania, puertorico, rhodeisland, southcarolina, southdakota, tennessee, texas, utah, vermont, virginislands, virginia, washington, westvirginia, wisconsin, wyoming = saved_export['HTML'].to_list()

soup_dictionary = {}
for state in saved_export['HTML']:
    # MAKE A VARIABLE TO CONTAIN ALL OF THE CONTENTS
    individual_page_contents = state

    # MAKE IT BEAUTIFUL USING THE LIBRARY ABOVE
    beautifulContents = BeautifulSoup(individual_page_contents, "lxml")

    # PARSE HTML Content
    html = beautifulContents.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    soup_dictionary[state] = soup

# GET EXAM REQUIREMENTS

exam_requirements = {}
for state in soup_dictionary.keys():
    text = soup_dictionary[state].find("div", class_="p4")
    text =  re.sub(r'<.+?>', '', str(text))
    text =  text.replace('\n','')
    text = re.sub(' +', ' ', text)
    exam_requirements[state] = text
    
pprint.pprint(exam_requirements[wisconsin])

exam_requirements = pd.DataFrame.from_dict([exam_requirements])
exam_requirements = exam_requirements.transpose()
exam_requirements.set_index(state_links_df['State'],inplace=True)

exam_requirements.to_excel('nasba_webscrape/state_exam_requirements.xlsx')
state_links_df.to_excel('nasba_webscrape/state_links.xlsx')