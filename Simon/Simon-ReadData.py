import sqlite3
import os
import json
import matplotlib.pyplot as plt

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def doCalc(filename):
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    cur, conn = setUpDatabase('balldontlie.db')
    db_data = cur.execute('SELECT Pitchers.era, Pitchers.whip, IDs.hand FROM Pitchers JOIN IDs ON Pitchers.player_id = IDs.player_id').fetchall()

    # get averages
    l_era = []
    l_whip = []
    r_era = []
    r_whip = []
    for pair in db_data:
        if pair[2] == 'R':
            r_era.append(pair[0])
            r_whip.append(pair[1])
        else:
            l_era.append(pair[0])
            l_whip.append(pair[1])

    data['Baseball'] = {'ERA': {'Left': sum(l_era)/len(l_era), 'Right': sum(r_era)/len(r_era)}, 
    'WHIP': {'Left': sum(l_whip)/len(l_whip), 'Right': sum(r_whip)/len(r_whip)}}

    with open(filename, 'w') as f:
        json.dump(data, f)
    
    
def showViz(filename):
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)

    data = data['Baseball']
    x = data['ERA'].keys()
    y = data['ERA'].values()

    ax1.bar(x, y, align='center', alpha=0.5)
    ax1.set(xlabel='Average ERA', ylabel='Hand', title='Average ERA for Right vs. Left Handed Pitchers')

    x = data['WHIP'].keys()
    y = data['WHIP'].values()

    ax2.bar(x, y, align='center', alpha=0.5)
    ax2.set(xlabel='Average WHIP', ylabel='Hand', title='Average WHIP for Right vs. Left Handed Pitchers')

    plt.show()

if __name__ == '__main__':
    # doCalc('data.json')
    showViz('data.json')