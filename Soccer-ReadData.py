import matplotlib.pyplot as plt
import sqlite3
import os
import json


def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def doCalc(filename):
    '''
    Do the Calculations:
    - Get the average height of each player by position (0-3)
    Input is json file that hold data
    New calculations then outputted to json file as new key 'Soccer'
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
       data = json.load(jsonFile)
    

    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('SELECT height, position FROM Players')

    player_heights = cur.fetchall()
    defender = []
    attacker = []
    goalie = []
    mid = []
    for val in player_heights:
        if val[1] == 0:
            attacker.append(val[0])
        elif val[1] == 1:
            mid.append(val[0])
        elif val[1] == 2:
            defender.append(val[0])
        else:
            goalie.append(val[0])

    avg_attacker = sum(attacker) / len(attacker)
    avg_mid = sum(mid) / len(mid)
    avg_defender = sum(defender) / len(defender)
    avg_goalie = sum(goalie) / len(goalie)
    

    data['Soccer'] = {'Attacker': avg_attacker, 'Midfielder': avg_mid, 'Defender': avg_defender, 'Goalkeeper': avg_goalie}

    with open(full_path, 'w') as f:
       json.dump(data, f, indent=4)    
    

def showViz(filename):
    '''
    Create the visual
    Bar chart of heights by different position
    Input is json file with the data
    Output is the visual
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    heights = data['Soccer'].values()
    positions = data['Soccer'].keys()

    plt.bar(positions, heights, align='center', alpha=0.5, color=['blue'])
    plt.ylabel('Average Heights (cm)')
    plt.xlabel('Positions')
    plt.title('Average Heights By Position for Players in Premier League')
    plt.ylim(145, 195)

    plt.show()
 
if __name__ == '__main__':
    doCalc('data.json')
    showViz('data.json')
