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

def doCalc(filename, teams):
    '''
    Get average total game score for the team 
    Input: json file that holds data
    Input: List of team names that have data for.. if data does not exxist or spelled wrong, function will inform you
    Data then added and outputted to the json file as a new key  
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    full_path = os.path.join(os.path.dirname(__file__), filename)

    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)

    for team in teams:
        try:
            cur.execute(f'SELECT * FROM {team}')
        except:
            print(f'Table for {team} does not exist.. Check spelling')
            return

        result = cur.fetchall()
        total = 0
        count = 0
        for val in result:
            add = (val[2] + val[3])
            total += add
            count += 1
        avg = total / count


        data['Basketball'][team] = avg

        with open(full_path, 'w') as outfile:
            json.dump(data, outfile)
    showViz(filename)
    
def showViz(filename):
    '''
    Create a bar chart that shows average total game score for three teams
    team name on x axis
    average total game score on y axis
    Input is json file that holds the data needed for the bar charts
    Output is the bar chart
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)

    data = data['Basketball']

    teams = data.keys()
    values = data.values()

    plt.bar(teams, values, align='center', alpha=0.5)
    plt.ylabel(f'Average Total Game Score')
    plt.xlabel('Team Name')
    plt.title('Average Score')

    plt.show()

if __name__ == '__main__':
    doCalc('data.json', ['Knicks', 'Lakers'])