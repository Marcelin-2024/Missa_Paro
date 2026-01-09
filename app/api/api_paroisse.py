import datetime
from flask import request, jsonify
from app.api.api_fidele import api_bp
from module_paroisse import ajoute_paroisse


@api_bp.route('/paroisse', methods=['POST'])
def paroisse():
    data = request.get_json()
    if data:
        nom_complet = data.get("nom_complet", "")
        poste = data.get("poste", "")
        gmail = data.get("email", "")
        password = data.get("password", "")
        telephone = data.get("telephone", "")
        diocese = data.get("diocese", "")
        paroisse = data.get("paroisse", "")
        date = datetime.datetime.now().strftime("%d %m %Y %H:%M")
        ajoute_paroisse(nom_complet,diocese,paroisse,gmail,poste,password,telephone, date)
        return jsonify(success=True, data="donnée envoyée"), 201
    return jsonify(
        success=True,
        data="mauvais envoie du fichier json")