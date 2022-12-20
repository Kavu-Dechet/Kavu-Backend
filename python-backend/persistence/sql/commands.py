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
        longitude FLOAT        
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dechets_categories (
        dechet_categorie_id BIGSERIAL PRIMARY KEY,
        dechet_id BIGSERIAL,
        categorie VARCHAR(60),  
        CONSTRAINT fk_dechet
            FOREIGN KEY(dechet_id) 
            REFERENCES dechets(dechet_id)      
    )
    """,
    """
      CREATE TABLE IF NOT EXISTS actions_dechets (
          action_dechet_id BIGSERIAL PRIMARY KEY,
          dechet_categorie_id BIGSERIAL,
          statut VARCHAR(70),
          date_action DATE,
          utilisateur_id BIGSERIAL,
          CONSTRAINT fk_dechet
              FOREIGN KEY(dechet_categorie_id) 
              REFERENCES dechets_categories(dechet_categorie_id)
      )
      """,
)
#           CONSTRAINT fk_utilisateur
#               FOREIGN KEY(utilisateur_id)
#               REFERENCES utilisateurs_mobile(utilisateur_id)

INSERT_DECHET = """INSERT INTO dechets (latitude,longitude)
             VALUES(%s,%s)
             RETURNING dechet_id"""

INSERT_DECHET_CATEGORIE = """INSERT INTO dechets_categories (dechet_id,categorie)
             VALUES(%s,%s)
             RETURNING dechet_categorie_id"""

INSERT_ACTION_DECHET = """INSERT INTO actions_dechets (dechet_categorie_id, statut, date_action, utilisateur_id)
             VALUES(%s,%s,%s,%s)
             RETURNING action_dechet_id"""

DELETE_DECHET = """DELETE FROM dechets where id=%s"""

FETCH_DECHET = """SELECT actions_dechets.action_dechet_id, dechets.latitude, dechets.longitude, dechets_categories.categorie, actions_dechets.statut
                    FROM actions_dechets
                    INNER JOIN dechets_categories
                    ON dechets_categories.dechet_categorie_id=actions_dechets.dechet_categorie_id
                    INNER JOIN dechets
                    ON dechets.dechet_id=dechets_categories.dechet_id;
                """
