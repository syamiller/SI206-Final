import requests
import sqlite3
import os
import json
import time

''' 
Using MLB Data API
https://appac.github.io/mlb-data-api-docs/#top
Needs an API Key
'''

headers = {
        'x-rapidapi-key': "2ef16e9246msha6237e4233efa3bp10476fjsndfae9ee072e8",
        'x-rapidapi-host': "mlb-data.p.rapidapi.com"
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

def create_id_list():
    '''
    Returns a list of all of the team ids from the MLB in the API --> 30 teams
    Used in create_pitchers_list()
    '''
    url = "https://mlb-data.p.rapidapi.com/json/named.team_all_season.bam"

    querystring = {"season":"'2018'","all_star_sw":"'N'","sort_order":"league_full_asc"}

    response = requests.get(url, headers=headers, params=querystring)

    data = response.text
    dict_list = json.loads(data)['team_all_season']['queryResults']['row']

    id_list = []
    for team in dict_list:
        if team['league_full'] == 'National League' or team['league_full'] == 'American League':
            id_list.append(team['team_id'])
    return id_list

def create_id_table():
    '''
    Creates a table of player IDs
    Players only added to table if their position is pitcher
    Pitcher hand (0 or 1) is also a column in the table --> 0 is L, 1 is R
    10 new players added on each run by using a count
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS IDs (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, hand INTEGER)')
    team_list = create_id_list()
    count = 0
    url = "https://mlb-data.p.rapidapi.com/json/named.roster_team_alltime.bam"

    for team in team_list:
        querystring = {"end_season":"'2018'","team_id": int(team),"start_season":"'2018'","all_star_sw":"'N'","sort_order":"name_asc"}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.text
        dict_list = json.loads(data)['roster_team_alltime']['queryResults']['row']
        for player in dict_list:
            player_id = player['player_id']
            if player['primary_position'] == 'P':
                in_data = cur.execute('SELECT player_id FROM IDs WHERE player_id = ?', (player_id,)).fetchone()
                if in_data is not None:
                    continue
                hand = player['throws']
                if hand == 'L':
                    hand = 0
                else:
                    hand = 1
                cur.execute('INSERT OR IGNORE INTO IDs (player_id, hand) VALUES (?, ?)', (player_id, hand))
                conn.commit()
                count += 1

            if count == 10:
                print(f'{count} Pitchers Added!')
                return

    cur.close()

def create_table():
    '''
    Creates a table of Pitchers with there ERA and WHIP
    Pitchers only added to database if stats are available (cleaning)
    Max of 10 added at a time (but could be less) by using 'max(id)'
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Pitchers (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, era INTEGER, whip INTEGER)')

    # Figuring out where to start and end
    id_list = cur.execute('SELECT id, player_id FROM Pitchers ORDER BY id ASC').fetchall()
    if len(id_list) == 0:
        start = 0
    else:
        start_id = id_list[-1][-1]
        start = cur.execute('SELECT id FROM IDs WHERE player_id = ?', (start_id,)).fetchone()[0]
    max_id = cur.execute('SELECT MAX(id) FROM IDs').fetchone()[0]

    start += 1

    if start + 10 >= max_id:
        end = max_id + 1
    else:
        end = start + 10

    url = "https://mlb-data.p.rapidapi.com/json/named.sport_pitching_tm.bam"
    count = 0
    for i in range(start, end):
        player_id = cur.execute('SELECT player_id FROM IDs WHERE id = ?', (i,)).fetchone()[0]
        
        in_data = cur.execute('SELECT player_id FROM Pitchers WHERE player_id = ?', (player_id,)).fetchone()
        # check first to see if we already have data for that player
        if in_data is not None:
            print(f'Already have data for player {player_id}')
            continue
        # format request
        querystring = {"season":"'2018'","player_id": player_id,"league_list_id":"'mlb'","game_type":"'R'"}
        response = requests.get(url, headers=headers, params=querystring)

        # index through the data
        data = response.text
        stat_dict = json.loads(data)['sport_pitching_tm']['queryResults']

        # cleaning data -- checking to see if data from request for player is actually present
        if stat_dict['totalSize'] == "0":
            print(f'Player {player_id} has no data :(')
            continue
        elif isinstance(stat_dict['row'], list):
            print(f'Player {player_id} has no data :(')
            continue
        
        try:
            era = float(stat_dict['row']['era'])
            whip = float(stat_dict['row']['whip'])
        except:
            print(f'Player {player_id} has no data :(')
            continue

        if whip == 0.00 or era == 0.00:
            print(f'Player {player_id} has no data :(')
            continue
        
        cur.execute('INSERT OR IGNORE INTO Pitchers (player_id, era, whip) VALUES (? ,?, ?)', (player_id, era, whip))
        conn.commit()
        count += 1
    total = cur.execute('SELECT MAX(id) FROM Pitchers').fetchone()[0]
    cur.close()
    print(f'Added {count} pitchers!')
    print(f'{total} total players')

def main():
    '''
    Main driver of file
    Adds 10 pitchers to IDs table
    Then takes 15 second break before cleaning
    Then cleans and adds the pitchers to Pitchers Table
    '''
    create_id_table()
    print('Taking a quick break before cleaning!')
    time.sleep(15)
    create_table()
    print('Done! Wait 15 seconds before running again')


if __name__ == '__main__':
    main()
