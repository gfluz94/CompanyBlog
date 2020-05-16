import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required

from blog import db
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blog.users.pictures_handler import add_profile_pic

users_blueprint = Blueprint("users", __name__, template_folder="templates/users")

@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Log in successful!!")
            next = request.args.get("next")
            if next is None or next[0]=="/":
                next = url_for("core.index")
            return redirect(next)
    
    return render_template("login.html", form=form)


@users_blueprint.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for your registration!!")
        return redirect(url_for("users.login"))
    
    return render_template("register.html", form=form)


@users_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email

    profile_image = current_user.profile_image
    return render_template('update.html', profile_image=profile_image, form=form)


@users_blueprint.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)