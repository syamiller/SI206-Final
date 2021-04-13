import matplotlib
import sqlite3
import os


def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def doCalc():
    '''
    Do the Calculations:
    - Get avergae total game score for each of the three teams
    '''
    pass

def showViz():
    '''
    Create the visual
    Bar Graph:
    - team name on x axis
    - average total game score on y axis
    '''
    pass