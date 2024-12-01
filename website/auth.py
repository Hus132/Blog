#authentication related code goes here
#contains the routes . create a blueprint to store different routes here
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__) #create a blueprint with the name views.

@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        existing_user = User.query.filter_by(email = email).first()
        if existing_user:
            if check_password_hash(existing_user.password, password): #if the already hashed password in database equals to the plain password
                flash('Logged in!', category='success')
                login_user(existing_user,remember=True) #login in user through login manager and identify if user is logged in or not cause it stores data in session
            else: #in case passwords do not match
                flash('Password is incorrect!', category='error')
                return redirect(url_for('views.home'))
        else:
            flash('Email does not exist', category='error')
    return render_template('login.html', user = current_user) #pass the current user as a variable to the base html page for checking if the user is logged in or not
@auth.route('/sign-up', methods = ['GET','POST']) #define POSt request
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #checking if email and username alreday exist or not
        email_exists = User.query.filter_by(email = email).first()
        username_exists = User.query.filter_by(username = username).first()
        if email_exists:
            flash ('Email already registered', category= ' error')
        elif username_exists:
            flash('Username is already in use', category=' error')
        #check if passwords are matching
        elif password1 != password2:
            flash('paswords don\'t match!', category='error')
        elif len(password1) <6:
            flash('password is too short.', category='error')
        else:
            #create a new user and add to the database.
            #password must be hashed before it can be stored in the database.
            new_user = User (email = email, username=username, password = generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user) #add to session
            db.session.commit() # add to the database.
            login_user(new_user, remember=True) #login user right after account is created
            flash('user already created,')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user = current_user) #passing the user as a variable to check if user is logged in or not
@auth.route('/logout')
@login_required #this decorator means that this route can be accessed only if user is already logginin
def logout():
    logout_user()
    return redirect(url_for("views.home")) #redirect to view.home function not the url cause it might be changed.
