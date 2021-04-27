import requests
import sqlite3
import os
import json
import time
from bs4 import BeautifulSoup

'''
API-FOOTBALL
Documentation here --> https://www.api-football.com/documentation-v3#section/Introduction
This needs an API Key --> see below
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

    
def createPlayers():
    '''
    Create a players table with players from the EPL in the 2019 season
    - player_id is the id of that player given by the API
    - height is the height of the player in cm
    - posiiton is a number that correlates to the players position
    - - 0(attacker), 1(midfielder), 2(defender), 3(goalkeeper)
    '''

    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Players (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, height INTEGER , position INTEGER)')

    count = 0
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    for i in range(1, 34):
        querystring = {"league":"39","season":"2019","page":str(i)}
        r = requests.get(url, headers=headers, params=querystring)
        data = r.text
        dict_list = json.loads(data)['response']
        for player in dict_list:
            height = player['player']['height']
            if height is None: continue
            height = height.replace('cm', '')
            height = int(height)
            appearences = player['statistics'][0]['games']['appearences']
            position = player['statistics'][0]['games']['position']
            if position == 'Attacker':
                position = 0
            elif position == 'Midfielder':
                position = 1
            elif position == 'Defender':
                position = 2
            else:
                position = 3
            if appearences is None: continue
            player_id = player['player']['id']
            id_in_data = cur.execute('SELECT player_id FROM Players WHERE player_id = ?', (player_id,)).fetchone()
            if id_in_data is None and appearences >= 10:
                cur.execute('INSERT OR IGNORE INTO Players (player_id, height, position) VALUES (?, ?, ?)', (player_id, height, position))
                conn.commit()
                count += 1
                if count == 25:
                    print(f'Added {count} players!')
                    total = cur.execute('SELECT MAX(id) FROM Players').fetchone()[0]
                    print(f'{total} total players!')
                    print('Wait 30 seconds before running again!')
                    return
    

    
if __name__ == '__main__':
    createPlayers()
    
