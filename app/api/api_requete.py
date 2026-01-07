from flask import Blueprint, request, jsonify
from func_requete import ajoute_fidele, ajoute_intention
import datetime

api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

date = datetime.datetime.now().strftime("%d %m %Y %H:%M")

@api_bp.route('/fideles', methods=['POST'])
def fidel():
    data_json = request.get_json()
    if not date or 'data' in data_json:
        data = data_json['data']
        nom = data.get("nom", "")
        gmail = data.get("email", "")
        telephone = data.get("telephone", "")
        ajoute_fidele(nom, gmail, telephone, date)
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data={
            "mauvais envoie du fichier json"
        }
    )


@api_bp.route('/intentions', methods=['POST'])
def intent():
    data_json = request.get_json()
    if not date or 'data' in data_json:
        data = data_json['data']
        fidele_id = data.get("fidele_id", "")
        messe_id = data.get("messe_id", "")
        type_intention = data.get("type_intention", "")
        ajoute_intention(fidele_id,messe_id,type_intention,date)
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data={
            "mauvais envoie du fichier json"
        }
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