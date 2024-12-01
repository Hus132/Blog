#contains the routes . create a blueprint to store different routes here
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post,User, Comment
from . import db
views = Blueprint("views", __name__) #create a blueprint with the name views.


@views.route('/')
@views.route('/home')
@login_required # restrict access to hom epage unless user is logged in
def home():
    posts = Post.query.all()
    return render_template('home.html', user = current_user, posts = posts)

@views.route('/create-post',methods = ['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category= 'error')
        else:
            post = Post(text=text,author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user = current_user)

#a view that can delete a post.

@views.route('/delete-post/<id>') #adding a variab;le to the path <name_of_var>
@login_required
def delete_post(id):
    post = Post.query.filter_by(id = id).first() #filter the post by id
    if not post:
        flash('post does not exist.', category='error')
    elif current_user.id != post.id:
        flash('no permission to delete the post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('post deleted.',category='success')

    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def show_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('no user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    posts = user.posts
    return render_template('post.html', user=current_user, posts=posts,username=username)


@views.route('/create-comment/<post_id>', methods = ["POST"])
@login_required
def create_comment(post_id): #the parameter passed here should match the one passed to the route
    text = request.form.get('text')

    if not text:
        flash('comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text = text, author = current_user.id, post_id= post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    #first check if the comment exists
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('comment does not exist', category='error')
    #check if the user is authorized to delete the comment
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('you do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.home'))






    




