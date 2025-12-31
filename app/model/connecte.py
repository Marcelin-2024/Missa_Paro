from flask import Blueprint, render_template

connecte_bp = Blueprint(
    'market_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)
@connecte_bp.route('/connect')
def compte():
        return render_template('compte.html')