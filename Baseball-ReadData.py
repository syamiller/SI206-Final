import sqlite3
import os
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


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
    total_era = []
    total_whip = []
    for pair in db_data:
        total_era.append(pair[0])
        total_whip.append(pair[1])
        if pair[2] == 1:
            r_era.append(pair[0])
            r_whip.append(pair[1])
        else:
            l_era.append(pair[0])
            l_whip.append(pair[1])

    data['Baseball'] = {'ERA': {'Left': sum(l_era)/len(l_era), 'Right': sum(r_era)/len(r_era)}, 
    'WHIP': {'Left': sum(l_whip)/len(l_whip), 'Right': sum(r_whip)/len(r_whip)}, 'Total': {'ERA': total_era, 'WHIP': total_whip}}

    with open(full_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    
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
    
    gs = gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()

    data = data['Baseball']
    x = data['ERA'].keys()
    y = data['ERA'].values()

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.bar(x, y, align='center', alpha=0.5, color=['yellow'])
    ax1.set(ylabel='Average ERA', xlabel='Hand', title='Average ERA for Right vs. Left Handed Pitchers in MLB')

    x = data['WHIP'].keys()
    y = data['WHIP'].values()

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.bar(x, y, align='center', alpha=0.5, color=['green'])
    ax2.set(ylabel='Average WHIP', xlabel='Hand', title='Average WHIP for Right vs. Left Handed Pitchers in MLB')

    ax3 = fig.add_subplot(gs[1, :])
    ax3.scatter(data['Total']['ERA'], data['Total']['WHIP'], color='grey')
    ax3.set(xlabel='ERA', ylabel='WHIP', title='Scatterplot of ERA vs. WHIP for All Pitchers')

    plt.show()


if __name__ == '__main__':
    doCalc('data.json')
    showViz('data.json')