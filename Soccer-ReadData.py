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
    id_list = cur.execute('SELECT country_id FROM Players').fetchall()

    counts_dict = {}

    for tup in id_list:
        counts_dict[tup[0]] = counts_dict.get(tup[0], 0) + 1

    sorted_countries = sorted(counts_dict.items(), key=lambda x: x[1], reverse = True)

    sorted_counts_dict = {}
    for tup in sorted_countries[:7]:
        sorted_counts_dict[tup[0]] = tup[1]  

    total = sum(sorted_counts_dict.values())
    title_dict = {}
    for key in sorted_counts_dict.keys():
        country = cur.execute('SELECT Title FROM Countries WHERE id = ?', (key,)).fetchone()[0]
        title_dict[country] = (sorted_counts_dict.get(key) / total) * 100
        
    data['Soccer'] = title_dict

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
    
    sizes = data['Soccer'].values()
    labels = data['Soccer'].keys()

    fig1, ax1 = plt.subplots()

    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.show()

if __name__ == '__main__':
    # doCalc('data.json')
    showViz('data.json')
