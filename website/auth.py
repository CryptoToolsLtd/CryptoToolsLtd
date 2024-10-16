from flask import Blueprint,render_template, request, flash,  redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth',__name__)

@auth.route('/login_up', methods = ['GET','POST'])
def login():
    #sign up----------------------------
    if request.method == 'POST' and 'name' in request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists.', category='error')
        elif len(name) < 3:
            flash('Name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Mail must be greater than 3 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Welcome to our page {}'.format(name), category='success')
            return redirect(url_for('auth.login'))
    
    #login------------------
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try it again!!', category='error_login')
        else:
            flash('Email does not exists', category='error_login')    
        
    return render_template('login_up.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
