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
    - Get number of players from each country
    '''
    with open(filename, 'r') as jsonFile:
       data = json.load(jsonFile)
    

    cur, conn = setUpDatabase('balldontlie.db')
    cur.execute('SELECT * FROM Players')

    player_heights = cur.fetchall()
    #print(player_heights)
    defender = 0
    defender_count = 0
    attacker = 0
    attacker_count = 0
    mid = 0
    mid_count = 0
    goalie = 0
    goalie_count = 0
    for val in player_heights:
        if val[2] == 0:
            attacker += val[1]
            attacker_count += 1
        elif val[2] == 1:
            mid += val[1]
            mid_count += 1
        elif val[2] == 2:
            defender += val[1]
            defender_count += 1
        else:
            goalie += val[1]
            goalie_count += 1
    avg_attacker = float(str(attacker/attacker_count)[:6])
    avg_mid = float(str(mid/mid_count)[:6])
    avg_defender = float(str(defender/defender_count)[:6])
    avg_goalie = float(str(goalie/goalie_count)[:6])
    #print(avg_attacker, avg_defender, avg_goalie, avg_mid)
    
    avgs_d = {}
    avgs_d["Attacker"] = avg_attacker
    avgs_d["Midfielder"] = avg_mid
    avgs_d["Defender"] = avg_defender
    avgs_d["Goalkeeper"] = avg_goalie
    #print(avgs_d)

    data['Soccer'] = avgs_d

    with open(filename, 'w') as f:
       json.dump(data, f)    
    

def showViz(filename):
    '''
    Create the visual
    Pie:
    - 
    '''
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    heights = data['Soccer'].values()
    positions = data['Soccer'].keys()

    plt.bar(positions, heights, align='center', alpha=0.5)
    plt.ylabel('Average Heights (cm)')
    plt.xlabel('Positions')
    plt.title('Average Heights By Position')

    plt.show()
 
if __name__ == '__main__':
    #doCalc('data.json')
    showViz('data.json')
