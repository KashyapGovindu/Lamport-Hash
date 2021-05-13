import sqlite3
from sqlite3 import Error
import os
                                   
def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        print("Created mydatabase.db")
        return con 
    except Error:
        print("Error in creating database connection")

def sql_connectionSalt():
    try:
        con = sqlite3.connect('mydatabaseSalt.db')
        print("Created mydatabaseSalt.db")
        return con 
    except Error:
        print("Error in creating database connection")

def credentialsTable(connection,salt=None):
    cursorObj = connection.cursor()
    if salt is None:
        query =("CREATE TABLE IF NOT EXISTS clients "
                "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                "NAME VARCHAR(1024) NOT NULL, "
                "NVALUE INTEGER NOT NULL, "
                "PASSWORD VARCHAR(1024) NOT NULL)")
        # print(query)
        cursorObj.execute(query)
        print("Credentials Table creation successful")
    else:
        query =("CREATE TABLE IF NOT EXISTS clients "
                "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                "NAME VARCHAR(1024) NOT NULL, "
                "NVALUE INTEGER NOT NULL, "
                "PASSWORD VARCHAR(1024) NOT NULL, "
                "SALT VARCHAR(1024) NOT NULL)")
        # print(query)
        cursorObj.execute(query)
        print("Credentials Table creation successful")


def insertRecord(connection,object,salt=None):
    cursorObj = connection.cursor()
    if salt is None:
        query = """INSERT INTO clients (NAME, NVALUE, PASSWORD) VALUES (?,?,?)"""
        data = (object.username,object.n_value,object.password)
        # print(query)
        cursorObj.execute(query,data)
        connection.commit()
        print("Insert object into table successful")
    else:
        query = """INSERT INTO clients (NAME, NVALUE, PASSWORD, SALT) VALUES (?,?,?,?)"""
        data = (object.username,object.n_value,object.password,object.salt)
        # print(query)
        cursorObj.execute(query,data)
        connection.commit()
        print("Insert object into table successful")

def updateClientEntry(connection,object,salt=None):
    cursorObj = connection.cursor()
    if salt is None:
        query = """UPDATE clients SET NVALUE = ?, PASSWORD = ? WHERE NAME = ?"""
        data= (object.n_value,object.password,object.username)
        cursorObj.execute(query,data)
        connection.commit()
        print("Update object in table successful")
    else:
        query = """UPDATE clients SET NVALUE = ?, PASSWORD = ?, SALT = ? WHERE NAME = ?"""
        data= (object.n_value,object.password,object.salt,object.username)
        cursorObj.execute(query,data)
        connection.commit()
        print("Update object in table successful")

def selectClient(connection,object):
    cursorObj = connection.cursor()
    query = """SELECT * FROM clients WHERE NAME = ?"""
    data = (object.username,)
    cursorObj.execute(query,data)
    records = cursorObj.fetchone()
    print(records)





