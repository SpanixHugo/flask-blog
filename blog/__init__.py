from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import os, datetime
from .config.variables import SECRET_KEY

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_blog():
    blog = Flask(__name__)

    # CONFIG
    blog.config['SECRET_KEY'] = SECRET_KEY
    blog.config['BLOG_UPLOAD_PATH'] = os.path.join(BASE_DIR, "static/uploads/")
    blog.config['MAX_CONTENT_LENGTH'] = 2 * 1024 *1024

    # BLUEPRINT
    from .views.admin_auth import admin_auth
    blog.register_blueprint(admin_auth, url_prefix="/owner")

    from .views.category import category
    blog.register_blueprint(category, url_prefix="/owner")

    from .views.article import article
    blog.register_blueprint(article, url_prefix="/owner/article")

    # ERROR ROUTES
    # 404 - ERRORS
    @blog.errorhandler(404)
    def error_404(error):
        print("404 ERROR: ", str(error))
        return render_template("error-404.html")

    # 500 - ERROR
    # @blog.errorhandler(Exception)
    # def error_500(error):
    #     print("500 ERROR: ", str(error))
    #     return render_template("error-500.html")

    return blog