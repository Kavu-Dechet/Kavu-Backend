from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
from flasgger import Swagger

import persistence.crud_persistence as dechetsDAO
import persistence.images_persistence as imagesDAO
import json

from service.image_service import get_image

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
swagger = Swagger(app)


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
          categorie:
            type: string
    responses:
      200:
        description: La listes des déchets
    """
    result = dechetsDAO.query_all_dechets()
    if result:
        return jsonify(status="True",
                       result=[
                           {"id": actionDechet[0],
                            "latitude": actionDechet[1],
                            "longitude": actionDechet[2],
                            "categorie": actionDechet[3],
                            "type_action": actionDechet[4]} for actionDechet in result])
    return jsonify(status="False")


@app.route('/dechet/', methods=['POST'])
def create_dechet():
    """Publication d'un déchet
    Publie un déchet (lat,long et categorie). Note : Publication swagger non fonctionnelle ! Utiliser commande curl du README.md
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
      - name: categorie (non fonctionnelle)
        in: path
        type: string
        enum: ['all', 'VHU', 'D3E']
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
    if not validate_dechet(**payload):
        print("dechet invalid: " + str(payload))
        return jsonify(status='False', message='Dechet invalide: ' + str(payload))
    result = dechetsDAO.insert_dechet(**payload)

    if result:
        return jsonify(status='True', message='Dechet created')
    return jsonify(status='False')


@app.route('/dechet/<id>', methods=['DELETE'])
def delete_dechet(id):
    """Supprime un déchet
    Supprime un déchet
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Le déchet publier
        schema:
          $ref: '#/definitions/Dechet'
    """
    result = dechetsDAO.delete_dechet(id)

    if result:
        return jsonify(status='True', message='Dechet created')
    return jsonify(status='False')


@app.route('/photo/', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        print("Error: no photo attached")
        return redirect(request.url)
    file = request.files['photo']
    filename = imagesDAO.save_image(file)
    return redirect(url_for('upload_photo', filename=filename))


# TODO: move to new file
@app.route('/privacy-policy', methods=['GET'])
def get_privacy_policy():
    return render_template("privacy-policy.html")


@app.route('/geodechets', methods=['GET'])
def get_geodechets():
    """Récupérer les geoDechets
    Renvoit tous les déchets sous forme de geojson
    ---
    responses:
      200:
        description: La listes des geodéchets
    """
    result = dechetsDAO.query_all_dechets()
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {"geometry": {
                "type": "Point",
                "coordinates": [actionDechet[2], actionDechet[1]]
            },
                "type": "Feature",
                "properties": {
                    "categorie": actionDechet[3],
                    "type_action": actionDechet[4],
                    "popupContent": "Mayotte"
            },
                "id": actionDechet[0]
            } for actionDechet in result
        ]
    }
    return jsonify(geojson)


@app.route('/fake_geodechets', methods=['GET'])
def get_fake_geodechets():
    """Récupérer fake geoDechets
    Renvoit tous les déchets sous forme de geojson
    ---
    responses:
      200:
        description: La listes des geodéchets
    """
    with open("fake.geojson", "r") as file:
        content = file.read().replace("\n", "")
        return content


def validate_dechet(latitude, longitude, categories):
    return categories != "null" \
        and 44.92 <= float(longitude) <= 45.32 \
        and -13 <= float(latitude) <= -12.6

# categories

# image endpoint


@app.route('/category/image/<filename>')
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
    return get_image('./categories_images/', filename)


@app.route('/categories', methods=['GET'])
def categories():
    """Renvoie le json contenant toutes les categories de déchets et infos dessus.
    Renvoie un json contenant toutes les informations à propos des catégories de déchets.
    ---
    responses:
      200:
        description: un fichier json contenant un tableau. 

    """
    with open("trashCategoriesData.json", 'r') as jsonFile:
        jsonData = json.load(jsonFile)
        # print(type(jsonData[0]))
        return jsonify(jsonData)  # dumps : list of dict to json


if __name__ == '__main__':
    print("Hello from KavuDechet API")
    dechetsDAO.init()
    app.run(host='0.0.0.0', port=5000, debug=True)
