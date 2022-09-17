#!/usr/bin/python

import psycopg2

import persistence.config_persistence as config
from sql import commands
import random

connection = None


def init():
    global connection
    if not connection:
        connection = config.init_connection()


def query_all_dechets():
    cursor = connection.cursor()
    query = "SELECT * FROM dechets"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def insert_dechet(latitude, longitude, categorie):
    """ Insert un nouveau dechet"""
    try:
        # create a new cursor
        cur = connection.cursor()
        # execute the INSERT statement
        cur.execute(commands.INSERT_DECHET, (latitude, longitude, categorie))
        # commit the changes to the database
        connection.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur insertion")
        print(error)


def create_tables():
    """ create tables in the PostgreSQL database"""
    conn = None
    try:
        # # read the connection parameters
        # params = config()
        # # connect to the PostgreSQL server
        # conn = psycopg2.connect(**params)
        cur = connection.cursor()
        # create table one by one
        for command in commands.CREATE_TABLES:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur création")
        print(error)


if __name__ == '__main__':
    create_tables()
    insert_dechet(random.randint(0, 160), random.randint(0, 160), "VHU")
