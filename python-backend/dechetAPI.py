from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
from flasgger import Swagger
import json

from swagger import swagger_config, swagger_template
import libs.persistence.crud_persistence as dechetsDAO
import libs.persistence.images_persistence as imagesDAO
from libs.service.image_service import get_image
from libs.localisation.PointDansPolygone import trouver_commune
from assets.fake.fake import fakeData




app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
swagger = Swagger(app, config=swagger_config, template=swagger_template)


@app.route('/dechet/', methods=['GET'])
def get_all_dechets():
    """Récupérer tous les déchets
    Renvoit tous les déchets présents dans la base
    ---
    definitions:
      Dechet:
        type: object
        properties:
          latitude:
            type: integer
          longitude:
            type: integer
          category:
            type: string
    responses:
      200:
        description: La listes des déchets
    """
    # On récupère les déchets de la bdd
    result = dechetsDAO.query_all_dechets()
    
    if result:
        return jsonify(status="True",
                       result=[
                           {"id": actionDechet[0],
                            "latitude": actionDechet[1],
                            "longitude": actionDechet[2],
                            "category": actionDechet[3],
                            "commune": actionDechet[4],
                            "type_action": actionDechet[5]} for actionDechet in result])
    return jsonify(status="False")


@app.route('/dechet/', methods=['POST'])
def create_dechet():
    """Publication d'un déchet
    Publie un déchet (lat,long et category). Note : Publication swagger non fonctionnelle ! Utiliser commande curl du README.md
    ---
    parameters:
      - name: latitude (non fonctionnelle)
        in: path
        type: integer
        enum: ['all', '-12.824511', '89']
        required: true
        default: all
      - name: longitude (non fonctionnelle)
        in: path
        type: integer
        enum: ['all', '45.165455', '42']
        required: true
        default: all
      - name: categories (non fonctionnelle)
        in: path
        type: string
        enum: ['all', 'voiture', 'D3E']
        required: true
        default: all
    responses:
      200:
        description: Le déchet publié
        schema:
          $ref: '#/definitions/Dechet'
    """
    # On recupere le corps (payload) de la requete
    payload = request.form.to_dict()

    # On trouve le userId (42 quand il n'y en a pas)
    if "userhashid" in payload: # Temporary fix for version compatibility
        userId = payload["userhashid"]
    else:
        payload['userhashid'] = 42 # Temporary fix for version compatibility
        userId = 42
    
    # On valide le dechet (latitude, longitude, categories, userhashid)
    if not 'latitude' in payload:
        return jsonify(status='False', message='latitude manquante')
    if not 'longitude' in payload:
        return jsonify(status='False', message='longitude manquante')
    if not 'categories' in payload: 
        return jsonify(status='False', message='categories manquante')
    if payload['categories'] == "":
        return jsonify(status='False', message='categories vide')
    if not 'userhashid' in payload:
        return jsonify(status='False', message='userhashid manquant')
    
    # On vérifie que les coordonnées sont présentes correspondent à Mayotte
    # if not -13 <= float(payload['latitude']) <= -12.6:
    #     return jsonify(status='False', message='latitude invalide')
    # if not 44.92 <= float(payload['longitude']) <= 45.32:
    #     return jsonify(status='False', message='longitude invalide')
    
    # On insert le dechet
    latitude = payload["latitude"]
    longitude = payload['longitude']
    categories = payload['categories'] 
    
    commune = trouver_commune(latitude, longitude)
    result = dechetsDAO.insert_dechet(userId, latitude, longitude, commune, categories)

    # On retourne le résultat
    if result:
        return jsonify(status='True', message='Dechet created')
    
    return jsonify(status='False')


@app.route('/category/image/<filename>/', methods=['GET'])
def get_file(filename):
    """Renvoie l'image d'une catégorie
    Renvoie l'image servant d'icone pour une catégorie de déchets.
    ---
    parameters:
      - name: filename
        in: path
    responses:
      200:
        description: icone correspondant à la catégorie

    """
    return get_image('./assets/categories/images/', filename)


@app.route('/categories/', methods=['GET'])
def categories():
    """Renvoie le json contenant toutes les categories de déchets et infos dessus.
    Renvoie un json contenant toutes les informations à propos des catégories de déchets.
    ---
    responses:
      200:
        description: un fichier json contenant un tableau. 

    """
    with open("assets/categories/trashCategoriesData.json", 'r') as jsonFile:
        jsonData = json.load(jsonFile)
        return jsonify(jsonData)  # dumps : list of dict to json


@app.route('/fake_dechet/', methods=['GET'])
def fake_dechets():
    """Récupérer des données fakes pour le test.
    Renvois une liste d'objets json pour le test.
    ---
    responses:
      200:
        description: La listes des fake déchets
    """
    return jsonify(status='True', result=fakeData['fake'])

# @app.route('/dechet/<id>/', methods=['DELETE'])
# def delete_dechet(id):
#     """Supprime un déchet
#     Supprime un déchet
#     ---
#     parameters:
#       - name: id
#         in: path
#         type: integer
#     responses:
#       200:
#         description: Le déchet publier
#         schema:
#           $ref: '#/definitions/Dechet'
#     """
#     result = dechetsDAO.delete_dechet(id)

#     if result:
#         return jsonify(status='True', message='Dechet deleted')
#     return jsonify(status='False')


# @app.route('/photo/', methods=['POST'])
# def upload_photo():
#     if 'photo' not in request.files:
#         print("Error: no photo attached")
#         return redirect(request.url)
#     file = request.files['photo']
#     filename = imagesDAO.save_image(file)
#     return redirect(url_for('upload_photo', filename=filename))


# @app.route('/geodechets/', methods=['GET'])
# def get_geodechets():
#     """Récupérer les geoDechets
#     Renvoit tous les déchets sous forme de geojson
#     ---
#     responses:
#       200:
#         description: La listes des geodéchets
#     """
#     result = dechetsDAO.query_all_dechets()
#     geojson = {
#         "type": "FeatureCollection",
#         "features": [
#             {"geometry": {
#                 "type": "Point",
#                 "coordinates": [actionDechet[2], actionDechet[1]]
#             },
#                 "type": "Feature",
#                 "properties": {
#                     "category": actionDechet[3],
#                     "commune": actionDechet[4],
#                     "type_action": actionDechet[5],
#                     "popupContent": "Mayotte"
#                 },
#                 "id": actionDechet[0]
#             } for actionDechet in result
#         ]
#     }
#     return jsonify(geojson)







if __name__ == '__main__':
    print("Hello from KavuDechet API")
    dechetsDAO.init()
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("hello", app.__swagger__)
