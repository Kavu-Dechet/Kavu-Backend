CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS info (
        vendor_id BIGSERIAL PRIMARY KEY
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dechets (
        id SERIAL PRIMARY KEY,
        latitude FLOAT,
        longitude FLOAT,
        categorie VARCHAR(255)
    )
    """)

INSERT_DECHET = """INSERT INTO dechets (latitude,longitude, categorie)
             VALUES(%s,%s, %s)
             RETURNING id"""

DELETE_DECHET = """DELETE FROM dechets where id=%s"""
