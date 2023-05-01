CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS utilisateurs_mobile (
        utilisateur_id BIGSERIAL PRIMARY KEY
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dechets (
        dechet_id BIGSERIAL PRIMARY KEY,
        latitude FLOAT,
        longitude FLOAT,
        commune VARCHAR(128)        
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dechets_categories (
        dechet_categorie_id BIGSERIAL PRIMARY KEY,
        dechet_id BIGSERIAL,
        category VARCHAR(60),  
        CONSTRAINT fk_dechet
            FOREIGN KEY(dechet_id) 
            REFERENCES dechets(dechet_id)      
    )
    """,
    """
      CREATE TABLE IF NOT EXISTS actions_dechets (
          action_dechet_id BIGSERIAL PRIMARY KEY,
          dechet_categorie_id BIGSERIAL,
          type_action VARCHAR(70),
          date_action DATE,
          utilisateur_id BIGSERIAL,
          CONSTRAINT fk_dechet
              FOREIGN KEY(dechet_categorie_id) 
              REFERENCES dechets_categories(dechet_categorie_id)
      )
      """,
    """
  CREATE TABLE IF NOT EXISTS photos (
      photo_id BIGSERIAL PRIMARY KEY,
      photo_nom BIGSERIAL,
      verifiee BOOLEAN,
      path varchar(100),
      nom varchar(150)
  )
  """,
    """
  CREATE TABLE IF NOT EXISTS actions_photos (
      action_photo_id BIGSERIAL PRIMARY KEY,
      photo_id BIGSERIAL,
      action_id BIGSERIAL,
      CONSTRAINT fk_photo
          FOREIGN KEY(photo_id)
          REFERENCES photos(photo_id),
      CONSTRAINT fk_action
          FOREIGN KEY(action_id)
          REFERENCES actions_dechets(action_dechet_id)
  )
  """,
)
#           CONSTRAINT fk_utilisateur
#               FOREIGN KEY(utilisateur_id)
#               REFERENCES utilisateurs_mobile(utilisateur_id)

INSERT_DECHET = """INSERT INTO dechets (latitude,longitude, commune)
             VALUES(%s,%s,%s)
             RETURNING dechet_id"""

INSERT_DECHET_CATEGORIE = """INSERT INTO dechets_categories (dechet_id,category)
             VALUES(%s,%s)
             RETURNING dechet_categorie_id"""

INSERT_ACTION_DECHET = """INSERT INTO actions_dechets (dechet_categorie_id, type_action, date_action, utilisateur_id)
             VALUES(%s,%s,%s,%s)
             RETURNING action_dechet_id"""

DELETE_DECHET = """DELETE FROM dechets where id=%s"""

FETCH_DECHET = """SELECT actions_dechets.action_dechet_id, dechets.latitude, dechets.longitude, 
                    dechets_categories.category, dechets.commune, actions_dechets.type_action
                    FROM actions_dechets
                    INNER JOIN dechets_categories
                    ON dechets_categories.dechet_categorie_id=actions_dechets.dechet_categorie_id
                    INNER JOIN dechets
                    ON dechets.dechet_id=dechets_categories.dechet_id;
                """
