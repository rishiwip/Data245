# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 16:39:09 2021

@author: rishi
"""
import time
import cx_Oracle
import psycopg2 as pg
from datetime import timedelta
import cbpro
import pandas as pd
import string
recipeData         = []
ingredientData     = []
recipeStepsData    = []
#break_ct           = 100000
        
def postgresConnection():
    try:
        connection = pg.connect(
            host="localhost",
            user='postgres',
            password="Welcome123",
        )
        print('postgresConnection established...')
        return connection
    except Exception as e:
        print("Exception occurrred")
        print(str(e))
        
        
def loadData(data,s):
    try:
        sql = s
        conn = oracleConnection()
        c = conn.cursor()
        ct = 0
        for i in data:
            ct+=1
            #print(i)
            try:
                c.execute(sql,i)
            except Exception as e:
                print("Exception occurred while executing sql:",str(e))
                print(i)
                
            if ct % 1000 == 0:
                print(str(ct),' : rows processed')
                conn.commit()
            #print(i)
        print("Table Loaded successfully")
    except Exception as e:
        print("Exception occurred ")
        print(str(e))
        conn.rollback()
    finally:
        conn.commit()
        c.close()
        conn.close()
        print("Connection and Cursor Closed")
        
def processRecipeStats():
    import csv
    fileLoc = "C:/Users/rishi/OneDrive/Desktop/SJSU/245-Machine_Learning/Project/SourceData/Kaggle/"
    fName   = "epi_r_formatted.csv"
    ct = 0
    try:
        csv_file = open(fileLoc+fName, "r",encoding="utf8")
        reader = csv.reader(csv_file, delimiter=',',lineterminator="\n")
        next(reader)
        sql = "insert into RECIPEDB.RECIPE_LABELS VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        conn = postgresConnection()
        c = conn.cursor()
        for i in reader:  
            #print(i)
            ct+=1
            try:
                c.execute(sql,i)
            except Exception as e1:
                print(i)
                print("Exception happend while executing sql", str(e1))
                continue
            if ct % 1000 == 0:
                print(ct,' : rows processed')
        print("Table Loaded successfully")
    except Exception as e:
        print("Exception occurred ")
        print(str(e))
        #conn.rollback()
    finally:
        conn.commit()
        conn.close()
        print(str(ct),' : rows processed')
        print("Connection and Cursor Closed")



def main():
    global recipeData    
    global ingredientData   
    global recipeStepsData
    try:
        processRecipeStats()
    except Exception as e:
        print("Exception occurred",str(e))
    
if __name__ == '__main__':
    if main():
        True
    else:
        False
    