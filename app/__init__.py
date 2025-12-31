from flask import Flask, render_template
from app.api.key import api_bp
from app.model.connecte import connecte_bp


def App_Web(config_name):
    app = Flask(__name__)
    app.register_blueprint(connecte_bp, url_prefix='/page')
    app.register_blueprint(api_bp, url_prefix='/api')
    @app.route('/')
    def main():
        return render_template("login.html")
    return app