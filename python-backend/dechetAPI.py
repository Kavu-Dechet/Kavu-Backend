from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_cors import CORS
from flasgger import Swagger

import persistence.crud_persistence as dechetsDAO
import persistence.images_persistence as imagesDAO
import json

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
                           {"id": dechet[0],
                            "latitude": dechet[1],
                            "longitude": dechet[2],
                            "categorie": dechet[3]} for dechet in result])
    return jsonify(status="False")

@app.route('/dechet/', methods=['POST'])
def create_dechet():
    """Publication d'un déchet
    Publie un déchet (lat,long et categorie)
    ---
    parameters:
      - name: latitude
        in: path
        type: integer
        enum: ['all', '-12.824511', '89']
        required: true
        default: all
      - name: longitude
        in: path
        type: integer
        enum: ['all', '45.165455', '42']
        required: true
        default: all
      - name: categorie
        in: path
        type: string
        enum: ['all', 'VHU', 'D3E']
        required: true
        default: all
    responses:
      200:
        description: Le déchet publier
        schema:
          $ref: '#/definitions/Dechet'
    """
    # On recupere le corps (payload) de la requete
    payload = request.form.to_dict()
    result = dechetsDAO.insert_dechet(**payload)

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

#TODO: move to new file
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
    geojson={
        "type": "FeatureCollection",
        "features":[
       {"geometry": {
         "type": "Point",
         "coordinates": [dechet[1],dechet[2]]
         },
        "type": "Feature",
        "properties": {
            "popupContent": "Mayotte"
        },
        "id": dechet[0]
         } for dechet in result
        ]
    }
    return jsonify(geojson)

@app.route('/geodechets2', methods=['GET'])
def get_fake_geodechets():
    """Récupérer fake geoDechets
    Renvoit tous les déchets sosu forme de geojson
    ---
    responses:
      200:
        description: La listes des geodéchets
    """
    with open("fake.geojson","r") as file:
        content = file.read().replace("\n","")
        return content
if __name__ == '__main__':
    print("Hello from API")
    dechetsDAO.init()
    app.run(host='0.0.0.0', port=5000, debug=True)
