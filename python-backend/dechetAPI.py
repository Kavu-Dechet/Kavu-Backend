from flask import Flask, jsonify, request, redirect, url_for, render_template
import crud_persistence

import images_persistence

app = Flask(__name__)


@app.route('/dechet/', methods=['POST'])
def create_dechet():
    # On recupere le corps (payload) de la requete
    payload = request.form.to_dict()
    result = crud_persistence.insert_dechet(**payload)

    if result:
        return jsonify(status='True', message='Dechet created')
    return jsonify(status='False')


@app.route('/dechet/', methods=['GET'])
def get_all_dechets():
    result = crud_persistence.query_all_dechets()
    if result:
        return jsonify(status="True",
                       result=[
                           {"id": dechet[0],
                            "latitude": dechet[1],
                            "longitude": dechet[2],
                            "categorie": dechet[3]} for dechet in result])
    return jsonify(status="False")


@app.route('/photo/', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        print("Error: no photo attached")
        return redirect(request.url)
    file = request.files['photo']
    filename = images_persistence.save_image(file)
    return redirect(url_for('upload_photo', filename=filename))

#TODO: move to new file
@app.route('/privacy-policy', methods=['GET'])
def get_privacy_policy():
    return render_template("privacy-policy.html")

#TODO: move to new file
@app.route('/geodechets', methods=['GET'])
def get_geodechets():
    with open("fake.geojson","r") as file:
        content = file.read()
        print(content)
        return jsonify(content.replace("\n",""))

if __name__ == '__main__':
    print("Hello from API")
    crud_persistence.init()
    app.run(host='0.0.0.0', port=5000, debug=True)
