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
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
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
    cur, conn = setUpDatabase('baseball.db')
    cur.execute('DROP TABLE IDs')
    cur.execute('CREATE TABLE IF NOT EXISTS IDs (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE)')
    team_list = create_id_list()
    count = 0
    url = "https://mlb-data.p.rapidapi.com/json/named.roster_team_alltime.bam"

    for team in team_list:
        count += 1
        querystring = {"end_season":"'2018'","team_id": int(team),"start_season":"'2018'","all_star_sw":"'N'","sort_order":"name_asc"}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.text
        dict_list = json.loads(data)['roster_team_alltime']['queryResults']['row']
        for player in dict_list:
            if player['primary_position'] == 'P':
                cur.execute('INSERT OR IGNORE INTO IDs (player_id) VALUES (?)', (player['player_id'], ))
                conn.commit()
        if count == 15:
            print('Halftime! Taking a short break...')
            time.sleep(30)
    cur.close()

def create_table():
    cur, conn = setUpDatabase('baseball.db')
    cur.execute('CREATE TABLE IF NOT EXISTS Pitchers (id INTEGER PRIMARY KEY, player_id INTEGER UNIQUE, era INTEGER, whip INTEGER)')
    start = cur.execute('SELECT MAX(id) FROM Pitchers').fetchone()[0]
    max_id = cur.execute('SELECT MAX(id) FROM IDs').fetchone()[0]

    if start is None:
        start = 1
    elif start >= max_id:
        print('Already Done!')
        return
    else:
        diff = start % 25
        start = start + diff

    if start + 25 >= max_id:
        end = max_id
        print('Last time!')
    else:
        end = start + 25

    url = "https://mlb-data.p.rapidapi.com/json/named.sport_pitching_tm.bam"
    count = 0
    print(start)
    print(end)
    for i in range(start, end):
        player_id = cur.execute('SELECT player_id FROM IDs WHERE id = ?', (i,)).fetchone()[0]
        
        in_data = cur.execute('SELECT player_id FROM Pitchers WHERE player_id = ?', (player_id,)).fetchone()
        if in_data is not None:
            print(f'Already have data for player {player_id}')
            continue

        querystring = {"season":"'2018'","player_id": player_id,"league_list_id":"'mlb'","game_type":"'R'"}
        response = requests.get(url, headers=headers, params=querystring)

        data = response.text
        stat_dict = json.loads(data)['sport_pitching_tm']['queryResults']

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
    create_table()
