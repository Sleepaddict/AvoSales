# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:49:17 2020

@author: Lim Jun Hao
ref: https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
https://docs.python.org/2/library/sqlite3.html
"""
import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
import os

def create_connection():
    # create a connection object with the database file
    conn = None
    try:
        conn = sqlite3.connect('data\\2D.db')
    except Error as e:
        print(e)
        
    return conn

def get_regionlist(conn):
    df = pd.read_sql_query('''SELECT DISTINCT region FROM AvoGeo''', conn)
    region_list = df['region'].tolist()
    return region_list

def query_sales_by_region(conn, region):
    directory = "images/" + region + '.png'
    # check if graph already exists
    if not os.path.isdir(directory):
        # os.makedirs('../images/')        
        # execute SQL command to select relevant data first 
        df = pd.read_sql_query('''SELECT Date,
           strftime('%Y', Date) AS Year,
           strftime('%m', Date) AS Month,
           AveragePrice,
           sum(Type4046) AS Type4046,
           sum(Type4225) AS Type4225,
           sum(Type4770) AS Type4770,
           type,
           region
           FROM AvoGeo
           WHERE Year != "2018" AND 
           type = "conventional"
           GROUP BY Year,
              Month,
              Region ''', conn)
        # execute pandas command to select relevant dataframe
        df = df.loc[df['region'] == region]
        
        # prepare datapoints for each type of avocado
        y1 = df['Type4046'].tolist()
        y2 = df['Type4225'].tolist()
        y3 = df['Type4770'].tolist()
        x = df['Date'].tolist()
        
        # plot graph of sales
        fig, ax = plt.subplots(figsize=(15,8))
        
        plt.plot(x, y1, 'bo-', label = 'Type4046 Avocado')
        plt.plot(x, y2, 'go-', label = 'Type4225 Avocado')
        plt.plot(x, y3, 'ro-', label = 'Type4770 Avocado')
        plt.xlabel('Time')
        plt.ylabel('Avocado Sales')
        plt.title(region)
        plt.legend(loc='upper right')
        plt.tight_layout()
        # reduce number of x ticks to prevent overlap
        every_nth = 6
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        
        # save image to directory
        plt.savefig('images/' + region)
    
    