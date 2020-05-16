from flask import Blueprint, render_template, request
from blog.models import Post

core_blueprint = Blueprint("core", __name__, template_folder="templates/core")

@core_blueprint.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=posts)

@core_blueprint.route("/info")
def info():
    return render_template("info.html")