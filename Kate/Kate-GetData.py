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

    # DONE


def createWarriorsTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for Golden State Warriors. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IN NOT EXISTS Warrior (game_id INTEGER UNIQUE, home_team_score INTEGER, away_team_score)')
    base_url = 'https://balldontlie.io/api/v1/games?seasons[]=2018&team_ids[]=10&seasons[]=2017&postseason=false&page={}'

    # Each Request returns 25 games
    # There are 7 pages
    for i in range(1,8):
        print(f'Retreieving games from page {i}')
        request_url = base_url.format(i)
        r = requests.get(request_url)
        data = r.text
        dict_list = json.loads(data)['data']

        # Look at example.json to see what dict_list will look like for each iteration
        # From here loop through each game in dict_list and add the game_id, home team score, and visitor
        # team score into the database
        for game in dict_list:
            continue #replace this with code


        conn.commit()     #commit the changes
        print('Taking a short break...')
        time.sleep(15)


def createSixersTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for the 76ers. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''

    # Do same thing as above but for 76ers (team_ids[]=23) in url now
    # make sure to create new table for them


def createRocketsTable():
    '''
    Get data for all regular season games from 2017 and 2018 seasons
    for the Rockets. Collecting game_id, home_team_score, away_team_score.
    Using get all games from API and only returning 25 at a time.
    '''

    # Do same thing as above but for 76ers (team_ids[]=10) in url now
    # make sure to create new table for them


# uncomment below lines when done
# createWarriorsTable()
# createSixersTable()
# createRocketsTable()