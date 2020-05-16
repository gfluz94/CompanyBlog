from flask import Blueprint, render_template, request

errors_blueprint = Blueprint("error_pages", __name__, template_folder="templates/errors")

@errors_blueprint.app_errorhandler(403)
def error403(e):
    return render_template("403.html"), 403

@errors_blueprint.app_errorhandler(404)
def error404(e):
    return render_template("404.html"), 404