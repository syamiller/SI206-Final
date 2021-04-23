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
    Do the Calculations:
    - Get average total game score for each of the three teams
    '''
    cur, conn = setUpDatabase('balldontlie.db')
    # full_path = os.path.join(os.path.dirname(__file__), filename)
    #WARRIORS
    cur.execute('SELECT * FROM Warrior')
    w_result = cur.fetchall()
    w_avg = 0
    w_count = 0
    for val in w_result:
        add = (val[2] + val[3])
        #print(add)
        w_avg += add
        w_count += 1
    w_final = w_avg/w_count
    
    #print("THIS IS THE WARRIORS' AVG")
    #print(w_final)
    #print('---------------------')


    #SIXERS
    cur.execute('SELECT * FROM Sixers')
    s_result = cur.fetchall()
    s_avg = 0
    s_count = 0
    for val in s_result:
        add = (val[2] + val[3])
        #print(add)
        s_avg += add
        s_count += 1
    s_final = s_avg/s_count
    
    #print("THIS IS THE SIXERS' AVG")
    #print(s_final)
    #print('---------------------')

    #ROCKETS
    cur.execute('SELECT * FROM Rockets')
    r_result = cur.fetchall()
    r_avg = 0
    r_count = 0
    for val in r_result:
        add = (val[2] + val[3])
        #print(add)
        r_avg += add
        r_count += 1
    r_final = r_avg/r_count
    
    #print("THIS IS THE ROCKETS' AVG")
    #print(r_final)
    #print('---------------------')

    #return (w_final, s_final, r_final)

    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)
    data['Basketball'] = {}
    data['Basketball']['Warriors'] = w_final
    data['Basketball']['Sixers'] = s_final
    data['Basketball']['Rockets'] = r_final
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    
def showViz(filename):
    '''
    Create the visual
    Bar Graph:
    - team name on x axis
    - average total game score on y axis
    '''
    with open(filename, 'r') as jsonFile:
        data = json.load(jsonFile)

    data = data['Basketball']

    teams = [i for i in data.keys()]
    values = [i for i in data.values()]

    plt.bar(teams, values, align='center', alpha=0.5)
    plt.ylabel('Average Total Game Score')
    plt.xlabel('Team Name')
    plt.title('Average Scores')

    plt.show()

if __name__ == '__main__':
    # doCalc('data.json')
    showViz('data.json')