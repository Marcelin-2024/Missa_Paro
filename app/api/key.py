from flask import Blueprint, render_template, json

api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)
@api_bp.route('/fideles', methods=["POST", "GET"])
def fidel():
    return { "success": True, "data": { "id": 1, "nom": "Kouassi Jean", "email": "jean@email.com", "telephone": "+22501020304" } }

@api_bp.route('intentions', methods=["POST", "GET"])
def intent():
        return {"success": True, "data": { "id": 12, "type_intention": "Défunts", "statut": "En attente" } }

@api_bp.route('/annonces', methods=["POST", "GET"])
def annon():
        return { "success": True, "data": [ { "id": 5, "titre": "Veillée de prière", "date_publication": "2024-03-20" } ] }
