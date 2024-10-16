from flask import Blueprint,render_template
from flask_login import login_required,current_user


views = Blueprint('views',__name__)

@views.route('/')
# @login_required
def home():
    return render_template ("home.html", user=current_user)

@views.route('/rsa')
@login_required
def rsa():
    return render_template("rsa.html", user=current_user)

@views.route('/elgamal')
@login_required
def elgamal():
    return render_template("elgamal.html", user=current_user)

@views.route('/elliptic')
@login_required
def elliptic():
    return render_template("elliptic.html", user=current_user)