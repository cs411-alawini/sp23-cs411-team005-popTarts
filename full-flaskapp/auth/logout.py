from flask import Blueprint, redirect, url_for, session

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route('/logout')
def logout():

    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login.login'))