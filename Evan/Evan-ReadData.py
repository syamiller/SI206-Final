import matplotlib
import sqlite3
import os


def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def doCalc(filename):
    '''
    Do the Calculations:
    - Get number of players from each country
    '''
    with open(filename, 'r') as jsonFile:
        data = json.load(filename)
    

    cur, conn = setUpDatabase('balldontlie.db')
    id_list = cur.execute('SELECT * FROM Players').fetchall()

    counts_dict = {}

    for tup in id_list:
        counts_dict[tup[2]] = counts_dict.get(tup[2], 0) + 1

    data['Soccer'] = {} # sorted dictionary

    with open(filename, 'w') as f:
        json.dump(data, f)    
    

def showViz():
    '''
    Create the visual
    Bar Graph:
    - country name on x axis
    - number of players on y axis
    '''
    pass

if __name__ == '__main__':
    doCalc('data.json')