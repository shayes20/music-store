import logging
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for

from app.database import get_db_connection
from .session import get_user

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET"])
@login_bp.route("/login.html", methods=["GET"])
def login() -> str:
    user = get_user()

    if user is None:
        return render_template("login.html")
    return redirect(url_for("index.index"))


@login_bp.route("/login", methods=["POST"])
@login_bp.route("/login.html", methods=["POST"])
def post() -> str:
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Missing username or password")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM users WHERE username = %s AND password = %s", (username, password))
                
                count = cur.fetchone()[0]

                if not count:
                    return render_template("Invalid username or password")

                session_id = uuid.uuid4().hex
                expiration_time = datetime.now() + timedelta(hours=6)

                cur.execute("INSERT INTO sessions (session_id, username, expiration) VALUES (%s, %s, %s)", (session_id, username, expiration_time))

                response = redirect(url_for("index.index"))
                response.set_cookie("session_id", session_id, expires=expiration_time)

                return response
    except Exception as e:
        logging.error(e)

        return render_template("login.html", error=e)
