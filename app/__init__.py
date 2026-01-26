import json
import os

from flask import Flask, render_template, current_app
from app.api.api_fidele import api_bp
from app.model.connecte import connecte_bp
from app.api.api_page import refresh_bp


def App_Web(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_J7kL9mN2bV4cX6zB8nM1qW3eR5tY7'
    app.register_blueprint(connecte_bp, url_prefix='/page')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(refresh_bp, url_prefix='/refresh')
    @app.route('/')
    def main():
        json_path = os.path.join(current_app.root_path, 'static/json/login.json')

        with open(json_path, 'r', encoding='utf-8') as f:
            form_data = json.load(f)

        # On envoie la liste des champs au template
        return render_template('compte.html', champs=form_data['connection'])
    return app