from flask import Blueprint, render_template
from ..config.database import get_connection

admin_auth = Blueprint("admin_auth", __name__)
get_connection()

@admin_auth.get("/")
def login_page():
    return render_template("/admin/login.html")

@admin_auth.get("/register")
@admin_auth.get("/sign-up")
def register_page():
    return render_template("/admin/register.html")