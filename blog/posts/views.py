from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from blog.posts.forms import BlogForm
from blog.models import Post, User
from blog import db

posts_blueprint = Blueprint("posts", __name__, template_folder="templates/posts")

@posts_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogForm()

    if form.validate_on_submit():

        title = form.title.data
        text = form.text.data

        post = Post(title, text, current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Blog post created!")

        return redirect(url_for("core.index"))

    return render_template("create.html", form=form)


@posts_blueprint.route("/<int:blog_post_id>")
def view_post(blog_post_id):
    post = Post.query.get_or_404(blog_post_id)
    return render_template("blogpost.html", post=post)


@posts_blueprint.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(blog_post_id):
    post = Post.query.get_or_404(blog_post_id)
    
    if post.author!=current_user:
        abort(403)

    form = BlogForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash("Blog post updated!")

        return redirect(url_for("posts.view_post", blog_post_id=post.id))

    return render_template("update_post.html", form=form)


@posts_blueprint.route("/<int:blog_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(blog_post_id):
    post = Post.query.get_or_404(blog_post_id)
    
    if post.author!=current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Blog post successfully deleted!")

    return redirect(url_for("core.index"))
