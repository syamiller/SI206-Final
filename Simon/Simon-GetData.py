import requests
import sqlite3
import os
import json
import time

headers = {
        'x-rapidapi-key': "2ef16e9246msha6237e4233efa3bp10476fjsndfae9ee072e8",
        'x-rapidapi-host': "mlb-data.p.rapidapi.com"
        }

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def create_id_list():
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

def create_pitchers_list():
    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('CREATE TABLE IF NOT EXISTS IDs (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, hand TEXT)')
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

                cur.execute('INSERT OR IGNORE INTO IDs (player_id, hand) VALUES (?, ?)', (player_id, player['throws']))
                conn.commit()
                count += 1

            if count == 25:
                print(f'{count} Pitchers Added!')
                print('Wait 15 seconds before running again!\n')
                return

    cur.close()

def create_table():
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

    if start + 25 >= max_id:
        end = max_id + 1
    else:
        end = start + 25

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
    cur.close()
    print(f'Added {count} pitchers!')


if __name__ == '__main__':
    # create_pitchers_list()
    # create_pitchers_list()
    # print('Taking a quit break before cleaning!')
    # time.sleep(15)
    create_table()
