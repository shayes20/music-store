import logging
from flask import Blueprint, render_template, request, redirect, url_for

from app.database import get_db_connection
from .session import get_user

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["GET"])
@register_bp.route("/register.html", methods=["GET"])
def register() -> str:
    user = get_user()

    if user is None:
        return render_template("register.html")
    return redirect(url_for("index.index"))


@register_bp.route("/register", methods=["POST"])
@register_bp.route("/register.html", methods=["POST"])
def post() -> str:
    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        return render_template("register.html", error="Missing username or password")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username))
                count = cur.fetchone()[0]

                if count:
                    return render_template(
                        "register.html", error=f'User "{username}" already exists'
                    )

                cur.execute("INSERT INTO users (username, password) VALUES ( %s, %s)", (username, password)
                )
                cur.close()

                return redirect(url_for("login.login"))
    except Exception as e:
        logging.error(e)

        return render_template("register.html", error=e)
