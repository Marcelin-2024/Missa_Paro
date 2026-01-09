import json
from enum import nonmember

from flask import Blueprint, render_template, current_app, url_for, redirect, request
import os

from supabase_auth.helpers import parse_auth_otp_response

from app.model.requete_api import requet_envoie, requet_connec
from module_paroisse import ajoute_paroisse

connecte_bp = Blueprint(
    'connect_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)
@connecte_bp.route('/connection')
def login():
    # Chemin vers le fichier JSON
    json_path = os.path.join(current_app.root_path, 'static/json/login.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        form_data = json.load(f)

    # On envoie la liste des champs au template
    return render_template('compte.html', champs=form_data['connection'])


@connecte_bp.route('/inscription')
def inscription():
    # Chemin vers le fichier JSON
    json_path = os.path.join(current_app.root_path, 'static/json/login.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        form_data = json.load(f)

    # On envoie la liste des champs au template
    return render_template('inscription.html', champs=form_data['inscription_champs'])


@connecte_bp.route('/Valide', methods=["POST"])
def chargement():
    paroisse = request.form.get('paroisse')
    diocese = request.form.get('diocese')
    nom_complet = request.form.get('nom_complet')
    poste = request.form.get('poste')
    telephone = request.form.get('telephone')
    gmail = request.form.get('gmail')
    password = request.form.get('password')
    requet_envoie(paroisse,diocese,nom_complet,poste,telephone,gmail,password)
    return redirect(url_for('connect_bp.login'))



@connecte_bp.route('/Tableau_bords', methods=["POST"])
def bords():
    gmail = request.form.get('gmail')
    password = request.form.get('password')
    requet_connec(gmail,password)
    return redirect(url_for('connect_bp.login'))