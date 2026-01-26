from flask import Blueprint, render_template

refresh_bp = Blueprint(
    'refresh_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@refresh_bp.route('/refresh_firt')
def refresh_firt():
    # On peut récupérer des données dynamiques ici (DB / Firebase)

    return render_template('pagepart/contenue1.html')

@refresh_bp.route('/refresh_second')
def refresh_second():
    # On peut récupérer des données dynamiques ici (DB / Firebase)
    return render_template('pagepart/contenue2.html')

@refresh_bp.route('/refresh_third')
def refresh_third():
    # On peut récupérer des données dynamiques ici (DB / Firebase)
    return render_template('pagepart/contenue3.html')

@refresh_bp.route('/refresh_four')
def refresh_four():
    # On peut récupérer des données dynamiques ici (DB / Firebase)
    return render_template('pagepart/contenue4.html')