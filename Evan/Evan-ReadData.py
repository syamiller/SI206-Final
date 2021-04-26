import matplotlib as plt
import sqlite3
import os
import json
import numpy as np


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
        data = json.load(jsonFile)
    

    cur, conn = setUpDatabase('balldontlie.db')
    id_list = cur.execute('SELECT * FROM Players').fetchall()

    counts_dict = {}

    for tup in id_list:
        counts_dict[tup[2]] = counts_dict.get(tup[2], 0) + 1
    #print(counts_dict)
    sorted_countries = sorted(counts_dict.values(), reverse = True)
    #print(sorted_countries)
    sorted_counts_dict = {}
    total = 0
    for i in sorted_countries:
        total += i
    percents = []
    for i in sorted_countries: 
        percents.append(i/total*100)
    percents[0]=percents[0] - .000000000000004
    print(percents)
    count = -1
    for j in sorted_countries:
        count+= 1
        for i in counts_dict:
            if counts_dict[i] == j:
                sorted_counts_dict[i] = percents[count]
        
    print(sorted_counts_dict)
    
    data['Soccer'] = sorted_counts_dict 

    with open(filename, 'w') as f:
        json.dump(data, f)    
    

def showViz():
    '''
    Create the visual
    Bar Graph:
    - country name on x axis
    - number of players on y axis
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    id_list = cur.execute('SELECT * FROM Countries').fetchall()
    countries_list = []
    

    #with open(filename, 'r') as jsonFile:
    #    data = json.load(jsonFile)

    #data = data["Soccer"]
    y = np.array(data.values())
    #labels = need to go into countries table to get their names 

    plt.pie(y, labels = mylabels, shadow = True)
    plt.show()




if __name__ == '__main__':
    doCalc('data.json')
    #showViz()