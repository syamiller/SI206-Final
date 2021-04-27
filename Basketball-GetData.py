import requests
import sqlite3
import os
import json
import time

'''
balldontlie API
Read documentation here --> https://www.balldontlie.io/#introduction
No API key required
Rate Limit is 60 Per Minute --> Be Mindful of This
'''



def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def createGamesTable():
    ''' 
    Creates a table of all of the games from the 2017 and 2018 seasons for a team
    User Input is team name, must be spelled correctly or function will inform you that the team does not exist
    User also inputs a page number 1-7
    Output is the table
    Max of 25 games added per time as we limit the amount of games per page to 25
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    teams_url = 'https://balldontlie.io/api/v1/teams'
    r = requests.get(teams_url)
    data = r.text
    dict_list = json.loads(data)['data']
    
    team = str(input('Enter a team name: '))
    team_id = None
    for org in dict_list:
        if org['name'] == team:
            team_id = org['id']
            break
    if team_id is None: print('Sorry, invalid team name :(')

    print(f'Creating or Updating a table for {team}')
    cur.execute(f'CREATE TABLE IF NOT EXISTS {team} (id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE, home_team_score INTEGER, away_team_score INTEGER)')
    max_id = cur.execute(f'SELECT MAX(id) FROM {team}').fetchone()[0]
    if max_id is not None and max_id == 164:
        print('Database is full. All games retrieved!')
        return

    page = str(input(f'Enter a page number 1-7: '))

    base_url = 'https://balldontlie.io/api/v1/games?seasons[]=2018&team_ids[]={}&seasons[]=2017&postseason=false&page={}'
    request_url = base_url.format(team_id, page)
    print(f'Retreieving games from page {page}')
    r = requests.get(request_url)
    data = r.text
    dict_list = json.loads(data)['data']

    if len(dict_list) == 0:
        print('Oops! Invalid page number!')
        return

    first_id = dict_list[0]['id']
    in_data = cur.execute(f'SELECT game_id FROM {team} WHERE game_id = ?', (first_id,)).fetchone()
    if in_data is not None:
        print(f'Already have data from page {page}! Run again and try a different page!')
        return
    
    for game in dict_list:
            game_id = game['id']
            home_score = game['home_team_score']
            visitor_score = game['visitor_team_score']
            cur.execute(f'INSERT OR IGNORE INTO {team} (game_id, home_team_score, away_team_score) VALUES (?, ?, ?)', (game_id, home_score, visitor_score))
            conn.commit()

    cur.close()

if __name__ == '__main__':
    createGamesTable()