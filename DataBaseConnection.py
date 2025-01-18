import sqlite3
import logging as log
import re

global DB
DB = dict() # empty dictionary


def connectToDB():
    # using global in order to modify the global variable otherwise it would only change it localy
    # wouldn't need global if  I was only reading
    global DB

    # connect to database (sqlite3.connect()) and to the results (sqlite3.Row) 
    conn = sqlite3.connect('Oscars.db', check_same_thread = False)
    conn.row_factory = sqlite3.Row

    # creating inserting key, value of database connection and cursor into 
    # global dictionary DB 
    DB['conn'] = conn
    DB['cursor'] = conn.cursor()

    # log print regarding successfullness of database connection
    log.info('Successfully connected to Oscars database')



# args can be None so that the function can be execute either as
# execute(query, args) or execute(query)
def execute(query, args = None):
    global DB

    # substitute all '\s+' ocurrences for ' ' in string sql
    #query = re.sub('\s+',' ', query)
    #log.info('SQL: {} Args: {}'.format(query, args))
    if args is not None:
        return DB['cursor'].execute(query, args)
    
    return DB['cursor'].execute(query)

 
def closeConnectionToDB():
    global DB
    DB['conn'].close()