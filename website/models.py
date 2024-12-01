from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# add columns of the data we need from the user : email, username, password and the date of creation of the account.
class User(db.Model, UserMixin): #usermixin helps in users loging in and out. main class in flask_login
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone = True), default = func.now()) #gives the current time value
    # how can I access the post related to each user in the user table ?
    posts = db.relationship('Post', backref = 'user', passive_deletes=True)# put the name of the table the post is referencing
    comments = db.relationship('Comment', backref='user', passive_deletes=True)                                                                      #backref means to access user its post.user e.g. post.user.username will give the username of the post creator.
                                                                            #passive_deletes means the posts are deleted when the user object is deleted


#create the class for Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # gives the current time value
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False) #db.Foreignkey is a way to establish a relationship between two tables.
    comments = db.relationship('Comment', backref='post', passive_deletes=True)                                                                                # in this case the author is checking if its number is equal to the number of user.id in the users table
                                                                                    # to check which user is the author of the corresponding post. Ondelete makes sure that when a user is deleted all the posts associated with the account are also deleted.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    text = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # gives the current time value
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

#the one to many relationship here basically is that a user has many posts and manmy comments associated with that post.
#a post can have many comments
# a comment has author and post id associated with it.