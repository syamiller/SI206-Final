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
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

    # DONE


def createWarriorsTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for Golden State Warriors. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Warrior (id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE, home_team_score INTEGER, away_team_score INTEGER)')
    base_url = 'https://balldontlie.io/api/v1/games?seasons[]=2018&team_ids[]=10&seasons[]=2017&postseason=false&page={}'


    max_id = cur.execute('SELECT MAX(id) FROM Warrior').fetchone()[0]
    if max_id is not None and max_id == 164:
        print('Database is full. All games retrieved!')
        return
    
    print('Updating Warriors Table')
    page = str(input('Enter a page number 1-7: '))
    print(f'Retreieving games from page {page}')
    
    request_url = base_url.format(page)
    r = requests.get(request_url)
    data = r.text
    dict_list = json.loads(data)['data']

    if len(dict_list) == 0:
        print('Oops! Invalid page number!')
        return

    first_id = dict_list[0]['id']
    in_data = cur.execute('SELECT game_id FROM Warrior WHERE game_id = ?', (first_id,)).fetchone()
    if in_data is not None:
        print(f'Already have data from page {page}! Run again and try a different page!')
        return
    
    for game in dict_list:
            #replace this with code
            game_id = game['id']
            home_score = game['home_team_score']
            visitor_score = game['visitor_team_score']
            cur.execute('INSERT OR IGNORE INTO Warrior (game_id, home_team_score, away_team_score) VALUES (?, ?, ?)', (game_id, home_score, visitor_score))
            conn.commit()

    cur.close()

def createSixersTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for the 76ers. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''

    # Do same thing as above but for 76ers (team_ids[]=23) in url now
    # make sure to create new table for them

    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Sixers (id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE, home_team_score INTEGER, away_team_score INTEGER)')
    base_url = 'https://balldontlie.io/api/v1/games?seasons[]=2018&team_ids[]=23&seasons[]=2017&postseason=false&page={}'

    max_id = cur.execute('SELECT MAX(id) FROM Sixers').fetchone()[0]
    if max_id is not None and max_id == 164:
        print('Database is full. All games retrieved!')
        return
    
    print('Updating Sixers Table')
    page = str(input('Enter a page number 1-7: '))
    print(f'Retreieving games from page {page}')
    
    request_url = base_url.format(page)
    r = requests.get(request_url)
    data = r.text
    dict_list = json.loads(data)['data']

    if len(dict_list) == 0:
        print('Oops! Invalid page number!')
        return

    first_id = dict_list[0]['id']
    in_data = cur.execute('SELECT game_id FROM Sixers WHERE game_id = ?', (first_id,)).fetchone()
    if in_data is not None:
        print(f'Already have data from page {page}! Run again and try a different page!')
        return
    
    for game in dict_list:
            #replace this with code
            game_id = game['id']
            home_score = game['home_team_score']
            visitor_score = game['visitor_team_score']
            cur.execute('INSERT OR IGNORE INTO Sixers (game_id, home_team_score, away_team_score) VALUES (?, ?, ?)', (game_id, home_score, visitor_score))
            conn.commit()

    cur.close()

def createRocketsTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for the Rockets. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''

    # Do same thing as above but for Rockets (team_ids[]=11) in url now
    # make sure to create new table for them
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Rockets (id INTEGER PRIMARY KEY, game_id INTEGER UNIQUE, home_team_score INTEGER, away_team_score INTEGER)')
    base_url = 'https://balldontlie.io/api/v1/games?seasons[]=2018&team_ids[]=11&seasons[]=2017&postseason=false&page={}'

    max_id = cur.execute('SELECT MAX(id) FROM Rockets').fetchone()[0]
    if max_id is not None and max_id == 164:
        print('Database is full. All games retrieved!')
        return
    
    print('Updating Rockets Table')
    page = str(input('Enter a page number 1-7: '))
    print(f'Retreieving games from page {page}')
    
    request_url = base_url.format(page)
    r = requests.get(request_url)
    data = r.text
    dict_list = json.loads(data)['data']

    if len(dict_list) == 0:
        print('Oops! Invalid page number!')
        return

    first_id = dict_list[0]['id']
    in_data = cur.execute('SELECT game_id FROM Rockets WHERE game_id = ?', (first_id,)).fetchone()
    if in_data is not None:
        print(f'Already have data from page {page}! Run again and try a different page!')
        return
    
    for game in dict_list:
            #replace this with code
            game_id = game['id']
            home_score = game['home_team_score']
            visitor_score = game['visitor_team_score']
            cur.execute('INSERT OR IGNORE INTO Rockets (game_id, home_team_score, away_team_score) VALUES (?, ?, ?)', (game_id, home_score, visitor_score))
            conn.commit()

    cur.close()


if __name__ == '__main__':
    # createWarriorsTable()
    # createSixersTable()
    createRocketsTable()