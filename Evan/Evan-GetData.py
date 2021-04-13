import requests
import sqlite3
import os
import json
import time
from bs4 import BeautifulSoup

'''
API-FOOTBALL
Documentation here --> https://www.api-football.com/documentation-v3#section/Introduction
This need an API Key --> see below
Keep in mind only allowed 100 requests per day (30 per minute)
'''

headers = {
    'x-rapidapi-key': "2ef16e9246msha6237e4233efa3bp10476fjsndfae9ee072e8",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createCountriesTable():
    '''
    This will create a cross reference table for the top 60 countries in soccer
    - id is an integery primary key that represents each country
    - title is the name of the country
    '''
    # create table
    cur, conn = setUpDatabase('Soccer')
    cur.execute('CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, title TEXT)')

    # get list of countries from website
    url = 'https://bleacherreport.com/articles/1573794-power-ranking-the-25-best-soccernations-based-on-per-capita'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', class_='blob')
    trs = table.find_all('tr')
    for tr in trs:
        tags = tr.find_all('td')
        title = tags[1].text.strip()
        cur.execute('INSERT OR IGNORE INTO Countries (title) VALUES (?)', (title,))
        conn.commit()

    # now we wont have duplicate strings when creating player database
    
def createPlayers():
    '''
    Create a players table with players from the EPL in the 2019 season
    - player_id is the id of that player given by the API
    - country_id is the id for the country that player was born in from the Countries table
    '''
    # Create Table
    cur, conn = setUpDatabase('Soccer')
    cur.execute('CREATE TABLE IF NOT EXISTS Players (player_id INTEGER PRIMARY KEY, country_id INTEGER)')

    
    # THIS IS AN EXAMPLE REQUEST YOU SHOULD USE
    # There are 33 total pages
    # Use this is a loop (described below)
    count = 1
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    querystring = {"league":"39","season":"2019","page":str(count)}
    r = requests.get(url, headers=headers, params=querystring)
    data = r.text
    dict_list = json.loads(data)['response']

    # an example of what dict_list looks like is in ex.json
    # Loop through this list of dictionaries and add players_id to table only if their country
    # is in the countries table and they have more than 10 appearances
    # NOTE: There may be mapping issues with the way some countries are spelled
    

# createCountriesTable()
createPlayers()