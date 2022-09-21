#!/usr/bin/python
from configparser import ConfigParser

import psycopg2
from persistence.sql import commands
import random

connection = None


def init_connection():
    params = config()
    global connection
    connection = psycopg2.connect(**params)
    create_tables()
    return connection

def create_tables():
    """ create tables in the PostgreSQL database"""
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


def config(filename='persistence/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
