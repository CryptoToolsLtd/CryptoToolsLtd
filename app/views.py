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

@views.route('/rsa_signature')
@login_required
def rsa_signature():
    return render_template("rsa_signature.html", user=current_user)

@views.route('/elgamal_signature')
@login_required
def elgamal_signature():
    return render_template("elgamal_signature.html", user=current_user)

@views.route('/elliptic_signature')
@login_required
def elliptic_signature():
    return render_template("elliptic_signature.html", user=current_user)

@views.route('/modulo')
@login_required
def modulo():
    return render_template("modulo.html", user=current_user)

@views.route('/is_prime')
@login_required
def is_prime():
    return render_template("is_prime.html", user=current_user)

@views.route('/jacobi_legendre')
@login_required
def jacobi_legendre():
    return render_template("jacobi_legendre.html", user=current_user)

@views.route('/contribute')
@login_required
def all_in_one():
    return render_template("contribute.html", user=current_user)

@views.route('/theory')
def theory():
    return render_template("theory.html", user=current_user)

@views.route('/diophantine')
def diophantine():
    return render_template("diophantine.html", user=current_user)
