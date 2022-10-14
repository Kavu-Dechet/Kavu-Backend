CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS Positions (
        positionId SERIAL PRIMARY KEY,
        category VARCHAR(255),
        description VARCHAR(255),
        coordinates POINT,
        area POLYGON
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS TrashCategories (
        trashCategoryId SERIAL PRIMARY KEY,
        name VARCHAR(255)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Partners (
        partnerId SERIAL PRIMARY KEY,
        name VARCHAR(255),
        description VARCHAR(255),
        mailAdress VARCHAR(255),
        phoneNumber VARCHAR(255),
        areas INTEGER[] REFERENCES Positions(positionId),
        interestingTrash INTEGER[] REFERENCES TrashCategories (trashCategoryId)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Messages (
        messageId SERIAL PRIMARY KEY,
        partner INTEGER REFERENCES Partners (partnerId),
        dateTime TIMESTAMP WITH TIME ZONE,
        messageText TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Chats (
        chatId SERIAL PRIMARY KEY,
        title VARCHAR(255),
        partner INTEGER REFERENCES Partners (partnerId),
        status INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ActionsOnTrash (
        actionOnTrashId SERIAL PRIMARY KEY,
        category VARCHAR(255),
        description VARCHAR(255),
        partners INTEGER[] REFERENCES Partners (partnerId),
        dateTime TIMESTAMP WITH TIME ZONE,
        pictures INTEGER[] REFERENCES Pictures (pictureId),
        chatId INTEGER REFERENCES Chats (chatId)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Trashs (
        trashId SERIAL PRIMARY KEY,
        location INTEGER REFERENCES Positions(positionId),
        categories INTEGER[] REFERENCES TrashCategories (trashId) ,
        userId INTEGER REFERENCES Users(userId),
        reporting INTEGER REFERENCES ActionsOnTrash(actionOnTrashId),
        actions INTEGER REFERENCES ActionsOnTrash(actionOnTrashId),
        closed INTEGER REFERENCES ActionsOnTrash(actionOnTrashId)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS Users (
        userId SERIAL PRIMARY KEY,
        userName VARCHAR(255),
        status INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Pictures (
        picturesId SERIAL PRIMARY KEY,
        userId INTEGER REFERENCES Users (userId),
        uri VARCHAR(255),
        publishable BOOLEAN
    )
    """)

INSERT_DECHET = """INSERT INTO dechets (latitude,longitude, categorie)
             VALUES(%s,%s, %s)
             RETURNING id"""

DELETE_DECHET = """DELETE FROM dechets where id=%s"""


"""
postgres type documentation :
geometric data types : https://www.postgresql.org/docs/11/datatype-geometric.html
- point : https://www.postgresql.org/docs/11/datatype-geometric.html#id-1.5.7.16.5
syntax :
( x , y )
  x , y

- polygon  : https://www.postgresql.org/docs/11/datatype-geometric.html#DATATYPE-POLYGON
syntax :
( ( x1 , y1 ) , ... , ( xn , yn ) )
  ( x1 , y1 ) , ... , ( xn , yn )
  ( x1 , y1   , ... ,   xn , yn )
    x1 , y1   , ... ,   xn , yn


"""
