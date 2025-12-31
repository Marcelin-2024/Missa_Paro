from flask import Blueprint

api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)
@api_bp.route('/key', methods=["POST"])
def key():
        return """"""