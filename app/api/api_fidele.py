from flask import Blueprint, request, jsonify
from module_fidele import *
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
        prenoms = data.get("prenoms", "")
        gmail = data.get("email", "")
        password = data.get("password", "")
        telephone = data.get("telephone", "")
        diocese = data.get("diocese", "")
        paroisse = data.get("paroisse", "")
        date = datetime.datetime.now().strftime("%d %m %Y %H:%M")
        nom_complet = nom+" "+prenoms
        ajoute_fidele(nom_complet,diocese,paroisse,gmail, password, telephone, date)
        return jsonify(success=True, data="donnée envoyée"), 201
    return jsonify(
        success=True,
        data="mauvais envoie du fichier json"

    )
@api_bp.route('/login', methods=['POST'])
def route_login():
    # Récupération des données envoyées par ton formulaire HTML/JS
    data = request.get_json()
    gmail = data.get('email') # 'gmail' car c'est le nom dans ton JSON
    password = data.get('password')
    resultat = connecter_utilisateur(gmail, password)
    if resultat["status"] == "success":
        # Ici, tu peux enregistrer l'uid dans la session Flask
        return jsonify(resultat), 200
    else:
        return jsonify(resultat), 401



@api_bp.route('/paroisse/<int:id>', methods=['GET'])
def get_paroisse(id):
    # Logique : Récupérer les infos d'une paroisse spécifique
    response = get_paroisse_db(id)
    return jsonify(response)

# --- MESSES & ANNONCES ---

@api_bp.route('/messes', methods=['GET'])
def get_messes():
    # Logique : Liste des horaires de messes
    reponse = get_messes_db()
    return jsonify(reponse)

@api_bp.route('/annonces', methods=['GET'])
def get_annonces():
    # Logique : Liste des dernières annonces
    reponse = get_annonces_db()
    return jsonify(reponse)

# --- INTENTIONS ---

@api_bp.route('/intentions', methods=['POST'])
def create_intention():
    # Logique : Créer une nouvelle intention de messe
    data_ = request.get_json()
    if data_:
        fidele_id = data_.get("fidele_id", "")
        messe_id = data_.get("messe_id", "")
        objet_intention = data_.get("objet_intention", "")
        detail_intention = data_.get("detail_intention", "")
        date = datetime.datetime.now().strftime("%d %m %Y %H:%M")
        post_intention(fidele_id,messe_id,objet_intention,detail_intention, date)
        return jsonify(success=True, data="donnée envoyée"), 201

    return jsonify(
        success=True,
        data="mauvais envoie du fichier json"
    )

@api_bp.route('/intentions/id', methods=['PUT'])
def update_intention(id):
    # Logique : Modifier une intention existante
    data_ = request.get_json()
    detail_intention = data_.get("detail_intention", "")
    object_intention = data_.get("objet_intention", "")
    update_intention_db(id,detail_intention,object_intention)
    return jsonify({"message": f"Intention {id} mise à jour"})

@api_bp.route('/intentions/<int:id>', methods=['DELETE'])
def delete_intention(id):
    # Logique : Supprimer une intention
    delete_intention_db(id)
    return jsonify({"message": f"Intention {id} supprimée"})

@api_bp.route('/intentions/mes/id', methods=['GET'])
def get_mes_intentions(id):
    # Logique : Liste des intentions de l'utilisateur connecté
    reponse = get_mes_intentions_db(fidele_id=id)
    return jsonify(reponse)

@api_bp.route('/intentions/validees', methods=['GET'])
def get_intentions_validees():
    # Logique : Liste des intentions approuvées par le curé
    reponse = get_intentions_validees_db()
    return jsonify(reponse)

# --- SYSTÈME & CONTACT ---

@api_bp.route('/notifications/registerPush', methods=['POST'])
def register_push():
    # Logique : Enregistrer le token pour les notifications mobiles
    return jsonify({"status": "Success", "token": "registered"})

@api_bp.route('/contact', methods=['POST'])
def contact():
    # Logique : Envoyer un message au secrétariat
    return jsonify({"message": "Message de contact bien reçu"})

@api_bp.route('/avis', methods=['POST'])
def post_avis():
    # Logique : Laisser un feedback sur l'application
    return jsonify({"message": "Merci pour votre note !"})