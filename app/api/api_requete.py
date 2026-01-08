from flask import Blueprint, request, jsonify
from func_requete import ajoute_fidele, ajoute_intention
import datetime

api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)



@api_bp.route('/fideles', methods=['POST'])
def fidel():
    data = request.get_json()
    if data:
        nom = data.get("nom", "")
        gmail = data.get("email", "")
        password = data.get("password", "")
        telephone = data.get("telephone", "")
        diocese = data.get("diocese", "")
        paroisse = data.get("paroisse", "")
        date = datetime.datetime.now().strftime("%d %m %Y %H:%M")
        ajoute_fidele(nom,diocese,paroisse,gmail, password, telephone, date)
        return jsonify(success=True, data="donnée envoyée"), 201
    return jsonify(
        success=True,
        data="mauvais envoie du fichier json"

    )


@api_bp.route('/intentions', methods=['POST'])
def intent():
    data_json = request.get_json()
    if not 'data' in data_json:
        data = data_json['data']
        fidele_id = data.get("fidele_id", "")
        messe_id = data.get("messe_id", "")
        type_intention = data.get("type_intention", "")
        date = datetime.datetime.now().strftime("%d %m %Y %H:%M")
        ajoute_intention(fidele_id,messe_id,type_intention,date)
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data="mauvais envoie du fichier json"
    )


@api_bp.route('/annonces', methods=['GET', 'POST'])
def annon():
    if request.method == 'POST':
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data=[
            {
                "id": 5,
                "titre": "Veillée de prière",
                "date_publication": "2024-03-20"
            }
        ]
    )

@api_bp.route('/messes', methods=['GET', 'POST'])
def messes():
    if request.method == 'POST':
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data=[
            {
                "id": 5,
                "titre": "Veillée de prière",
                "date_publication": "2024-03-20"
            }
        ]
    )