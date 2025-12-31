from flask import Flask, render_template
from app.model.connecte import connecte_bp


def App_Web(config_name):
    app = Flask(__name__)
    app.secret_key = "0102M@rco"
    app.register_blueprint(connecte_bp, url_prefix='/page')
    @app.route('/')
    def main():
        return render_template("login.html")
    return app