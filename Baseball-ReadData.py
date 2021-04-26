import sqlite3
import os
import json
import matplotlib.pyplot as plt

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
    Calculates average ERA and WHIP based on hand
    JOIN used in SELECT statement to get hand of pitcher
    Input: json file that holds data
    Data then added and outputted to the as a new key 
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    cur, conn = setUpDatabase('balldontlie.db')
    db_data = cur.execute('SELECT Pitchers.era, Pitchers.whip, IDs.hand FROM Pitchers JOIN IDs ON Pitchers.player_id = IDs.player_id').fetchall()

    # get averages
    l_era = []
    l_whip = []
    r_era = []
    r_whip = []
    for pair in db_data:
        if pair[2] == 1:
            r_era.append(pair[0])
            r_whip.append(pair[1])
        else:
            l_era.append(pair[0])
            l_whip.append(pair[1])

    data['Baseball'] = {'ERA': {'Left': sum(l_era)/len(l_era), 'Right': sum(r_era)/len(r_era)}, 
    'WHIP': {'Left': sum(l_whip)/len(l_whip), 'Right': sum(r_whip)/len(r_whip)}}

    with open(full_path, 'w') as f:
        json.dump(data, f)
    
    
def showViz(filename):
    ''' 
    Two bar charts created
    One shows average ERA for Right vs. Left Hand
    Other shows average WHIP for Right vs. Left Hand
    Input is json file that holds the data needed for the bar charts
    Output is the two bar charts
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)

    data = data['Baseball']
    x = data['ERA'].keys()
    y = data['ERA'].values()

    ax1.bar(x, y, align='center', alpha=0.5)
    ax1.set(xlabel='Average ERA', ylabel='Hand', title='Average ERA for Right vs. Left Handed Pitchers', ylim=(4.3, 5.5))

    x = data['WHIP'].keys()
    y = data['WHIP'].values()

    ax2.bar(x, y, align='center', alpha=0.5)
    ax2.set(xlabel='Average WHIP', ylabel='Hand', title='Average WHIP for Right vs. Left Handed Pitchers', ylim=(1.3, 1.6))

    plt.show()

if __name__ == '__main__':
    doCalc('data.json')
    showViz('data.json')