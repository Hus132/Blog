from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app(): #create a function to create the app and return it
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hello there"
    app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///C:\Users\Dom\PycharmProjects\lesson1\blog\website\database.db"
    db.init_app(app)

    from .views import views #import the views blueprint
    from .auth import auth


    app.register_blueprint(views, url_prefix= '/') #registed the blueprint with the app.
    app.register_blueprint(auth, url_prefix= '/')
 #import all the models that need to be created before the creation of the app.
    from .models import User, Post, Comment

    create_database(app) #whatever models we imported will be created in the app.
#this is what allows us to lock users in and out of the website and make sure that everytime they come in
    #they don't have to type in their username and password and to control their access priv
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" #if someone if not logged in then redirect them to auth( blueprint
                                            #and to the login view that is defined in the auth blueprint
    login_manager.init_app(app)

    #create a function that allows to access values from database related to user based on given id
    @login_manager.user_loader #@loginmanager stores data (user's id) during a session while user is loggin in
    def load_user(id): #id here is used to access the user's data from database.
        return User.query.get(int(id)) #id is stored as a str and needs to be converted into int

    return app

#a function to create the database
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("created database")
