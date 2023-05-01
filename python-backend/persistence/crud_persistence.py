#!/usr/bin/python

import psycopg2

import persistence.config_persistence as config
from persistence.sql import commands
import random

connection = None


def init():
    global connection
    if not connection:
        connection = config.init_connection()


def query_all_dechets():
    cursor = connection.cursor()
    query = commands.FETCH_DECHET
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def insert_dechet(userId, latitude, longitude, commune, categories):
    """ Insert un nouveau dechet"""
    try:
        # create a new cursor
        cur = connection.cursor()
        # insertion du déchet
        cur.execute(commands.INSERT_DECHET, (latitude, longitude, commune))
        id_dechet = cur.fetchone()[0]

        for category in categories.split(","):
            cur.execute(commands.INSERT_DECHET_CATEGORIE, (id_dechet, category))
            id_dechet_categorie = cur.fetchone()[0]
            cur.execute(commands.INSERT_ACTION_DECHET, (id_dechet_categorie, "CREATION", None, userId))

        connection.commit()
        cur.close()
        return id
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur insertion")
        print(error)


def delete_dechet(id):
    """Supprime un dechet"""
    try:
        # create a new cursor
        cur = connection.cursor()
        # execute the INSERT statement
        cur.execute(commands.DELETE_DECHET, (id))
        # commit the changes to the database
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur supprission dechet : " + id)
        print(error)


if __name__ == '__main__':
    create_tables()
    insert_dechet(random.randint(0, 160), random.randint(0, 160), "VHU")
